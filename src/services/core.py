from typing import List, Optional, Tuple, Type, TypeVar, Set

import elasticsearch
import fastapi
from elasticsearch import AsyncElasticsearch

from core.constants import ElasticIndexes
from models.core import Model, GetMultiQueryParam
from models.params import Search, Filters

ModelType: Model = TypeVar('ModelType')
Id: str = TypeVar('Id')


class ElasticServiceBase:
    def __init__(
            self,
            model: Type[ModelType],
            index: ElasticIndexes,
            cache_service,
            db_service: AsyncElasticsearch
    ):
        self.model = model
        self.index = index.value
        self.cache = cache_service
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
        :param exclude_fields: поля, которые нужно исключить из выходной модели
        :return: полученный объект, преобразованный в pydantic-схему
        """
        model = model or self.model

        # TODO: добавить поиск в кэше
        # obj = await self.cache.get(_id)
        obj = None

        if not obj:
            try:
                obj: dict = (await self.db.get(self.index, _id, _source_includes=exclude_fields)).get(
                    '_source'
                )
                # TODO: добавить объект в кэш
            except elasticsearch.NotFoundError:
                raise fastapi.HTTPException(404, f'Объект с идентификатором {_id} не найден')

        obj = self._exclude_fields(obj, exclude_fields)

        result = model(**obj)

        return result

    def _exclude_fields(self, obj: dict, field_names: Optional[Set[str]] = None) -> dict:
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
        get_multi_params = self._pack_get_multi_params(query_params, **params)

        search_params = self._pack_search_params(search, filters)

        objects = await self.db.search(index=self.index, body=search_params, params=get_multi_params)

        count = objects.get('hits', {}).get('total', {}).get('value', 0)
        objects = objects.get('hits', {}).get('hits', [])

        results = [model(**i.get('_source')) for i in objects]

        return results, count

    def _pack_get_multi_params(self, query_params: GetMultiQueryParam, **params) -> dict:
        order = 'desc' if query_params.descending else 'asc'
        sort_by = f'{query_params.sort_by}:{order}'

        return {
            'size': query_params.rows_per_page,
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
