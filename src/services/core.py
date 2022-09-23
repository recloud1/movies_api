from typing import List, Optional, Tuple, Type, TypeVar

from models.core import Model

ModelType: Model = TypeVar('ModelType')
Id: str = TypeVar('Id')


class ElasticServiceBase:
    def __init__(self, model: Type[ModelType], index: str, cache_service, db_service):
        self.model = model
        self.index = index
        self.cache = cache_service
        self.db = db_service

    def get(self, _id: Id) -> Optional[ModelType]:
        """
        Получение информации о конкретном объекте из источника данных

        :param _id: идентификатор получаемого объекта
        :return: полученный объект, преобразованный в pydantic-схему
        """
        obj = await self.cache.get(_id)
        if not obj:
            obj = await self.db.get(_id)

        result = self.model(**obj)

        return result


class ElasticServicePaginatedBase(ElasticServiceBase):
    def get_multi(
            self, offset: int = 0,
            limit: Optional[int] = None
    ) -> Tuple[List[ModelType], Optional[int]]:
        pass
