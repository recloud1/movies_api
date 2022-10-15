from collections import defaultdict
from typing import List, Optional, Tuple, Type, TypeVar, Set

import elasticsearch
import fastapi
from elasticsearch import AsyncElasticsearch

from core.constants import ElasticIndexes
from db.redis import RedisCache
from models.core import Model, GetMultiQueryParam
from models.params import Search, Filters

ModelType: Model = TypeVar('ModelType')
Id: str = TypeVar('Id')


class ElasticServiceBase:
    def __init__(
            self,
            model: Type[ModelType],
            index: ElasticIndexes,
            db_service: AsyncElasticsearch
    ):
        self.model = model
        self.index = index.value
        self.db = db_service

    async def get(
            self,
            _id: Id,
            model: Optional[ModelType] = None,
            exclude_fields: Optional[Set[str]] = None
    ) -> Optional[Model]:
        """
        Получение информации о конкретном объекте из источника данных

        :param _id: идентификатор получаемого объекта
        :param model: pydantic-схема данных (для возможного переопределения)
        :param exclude_fields: поля, которые нужно исключить из выходной модели
        :return: полученный объект, преобразованный в pydantic-схему
        """
        model = model or self.model
        try:
            obj: dict = (await self.db.get(index=self.index, id=_id, _source_includes=exclude_fields)).get(
                '_source'
            )
        except elasticsearch.NotFoundError:
            raise fastapi.HTTPException(404, f'Объект с идентификатором {_id} не найден')

        result = model(**obj)

        return result

    def _exclude_fields(self, obj: dict, field_names: Optional[Set[str]] = None) -> dict:
        """
        Исключение полей из результата запроса

        :param obj: объект из Elasticsearch
        :param field_names: коллекция наименования полей
        :return: объект, без полей, указанных в field_names
        """
        if not field_names:
            return obj

        result = {key: value for key, value in obj.items() if key not in field_names}

        return result


class ElasticServicePaginatedBase(ElasticServiceBase):
    async def get_multi(
            self,
            query_params: GetMultiQueryParam,
            search: Optional[Search] = None,
            filters: Optional[Filters] = None,
            model: Optional[ModelType] = None,
            **params
    ) -> Tuple[List[ModelType], Optional[int]]:
        """
        Получение списка объектов

        :param query_params: параметры пагинации
        :param search: значения для поиска
        :param filters: значения для фильтрации
        :param model: pydantic-схема для переопределения типа выходной модели
        :param params: дополнительные параметры
        :return: список объектов и общее количество объектов по запросу
        """
        model = model or self.model
        total_index_docs_count = (await self.db.count(index=self.index)).get('count')

        get_multi_params = self._pack_get_multi_params(query_params, total_index_docs_count, **params)

        search_params = self._pack_search_params(search, filters)

        objects = await self.db.search(index=self.index, body=search_params, params=get_multi_params)

        count = objects.get('hits', {}).get('total', {}).get('value', 0)
        objects = objects.get('hits', {}).get('hits', [])

        results = [model(**i.get('_source')) for i in objects]

        return results, count

    def _pack_get_multi_params(self, query_params: GetMultiQueryParam, total_count: int, **params) -> dict:
        order = 'desc' if query_params.descending else 'asc'
        sort_by = f'{query_params.sort_by}:{order}'
        size = query_params.rows_per_page if query_params.rows_per_page != 0 else total_count

        return {
            'size': size,
            'from': (query_params.page - 1) * (query_params.rows_per_page or 0),
            'sort': sort_by,
        }

    def _pack_search_params(self, search: Optional[Search], filters: Optional[Filters]) -> Optional[dict]:
        """
        Формирование объекта для поиска в Elasticsearch

        :param search: значения для поиска
        :param filters: значения для фильтрации
        :return:
        """
        filtering = [{'fuzzy': {i.field: i.value}} for i in filters.values] if filters else None
        filtering = {'filter': filtering} if filtering else {}

        matches = {i.field: i.value for i in search.values} if search else {}
        search_param = {
            'must': {
                'match': {
                    **matches
                }
            }
        } if matches else {}

        matches = {
            'bool': {
                **search_param,
                **filtering
            }
        } if search_param or filtering else None

        if not matches and not filtering:
            return {}

        return {'query': {**matches}}


class CachedElasticPaginated(ElasticServicePaginatedBase):
    def __init__(self, cache_service: RedisCache, expired_data_seconds: int, *args, **kwargs):
        self.cache_service = cache_service
        self.expired_data_seconds = expired_data_seconds
        super().__init__(*args, **kwargs)

    async def get(
            self,
            _id: Id,
            model: Optional[ModelType] = None,
            exclude_fields: Optional[Set[str]] = None
    ) -> Optional[Model]:
        key = self._generate_simple_key(str(self.__class__), _id)
        obj = await self.cache_service.get(key)
        if not obj:
            obj = await super().get(_id, model, exclude_fields)
            if obj:
                await self.cache_service.set(key, obj.dict(), expire_time_seconds=self.expired_data_seconds)

        return obj

    async def get_multi(
            self,
            query_params: GetMultiQueryParam,
            search: Optional[Search] = None,
            filters: Optional[Filters] = None,
            model: Optional[ModelType] = None,
            **params
    ) -> Tuple[List[ModelType], Optional[int]]:
        multi_cache_key = self._generate_multi_key(query_params, search, filters)
        result = await self.cache_service.get(multi_cache_key, default=[])
        count = len(result)

        if not result:
            result, count = await super().get_multi(query_params, search, filters, model, **params)

            if result:
                result_data = [i.dict() for i in result]
                await self.cache_service.set(
                    multi_cache_key,
                    result_data,
                    expire_time_seconds=self.expired_data_seconds
                )

        return result, count

    def _generate_multi_key(
            self,
            query_params: GetMultiQueryParam,
            search: Optional[Search] = None,
            filters: Optional[Filters] = None,
    ) -> str:
        """
        Генерация ключа в кэше для списка объектов

        :param query_params: параметры запроса
        :param search: параметры поиска в запросе
        :param filters: параметры фильтрации в запросе
        :return: ключ в виде строки
        """
        key_params = [
            str(self.__class__),
            str(query_params.page),
            str(query_params.rows_per_page),
            query_params.sort_by,
            str(query_params.descending),
        ]

        additional_key_params = lambda param: [f'{i.field}:{i.value}' for i in param.values]
        search_params = additional_key_params(search) if search else []
        filter_params = additional_key_params(filters) if search else []

        result_params = key_params + search_params + filter_params
        result = self._generate_simple_key(*result_params)

        return result

    def _generate_simple_key(self, *args) -> str:
        """
        Генерация ключа в кэше для единичного объекта

        :param args: параметры, которые нужно объединить в ключ
        :return: ключ в виде строки
        """
        result = ':'.join(args)
        return result
