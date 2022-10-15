from typing import List, TypeVar, Optional

import orjson
from pydantic import BaseModel, validator, Field
from pydantic.types import UUID4
from fastapi import Query


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Model(BaseModel):
    """Промежуточная модель pydantic'а для унифицирования конфигов и удобного администрирования"""

    class Config:
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


ListElement = TypeVar('ListElement', bound=Model)


class IdMixin(Model):
    """
    Миксин с полем Id для объектов.

    По своей сути крайне бесполезен, **однако** с помощью него можно задать порядок сортировки полей,
    сделав id первым полем в возвращаемых json объектах.

    Указывать первым справа, т.е. ``class YourModel(YourBaseModel, IdMixin)``
    """
    id: UUID4


class GetMultiQueryParam:
    def __init__(
            self,
            page: int = Query(
                default=1,
                ge=1,
                alias='page[number]',
                description='Текущая страница'
            ),
            rows_per_page: int = Query(
                default=25,
                ge=0,
                le=100,
                alias='page[size]',
                description='Количество объектов на одной странице'
            ),
            sort_by: str = Query(default='id', description='Поле сортировки результатов'),
            descending: bool = Query(default=False, description='Использовать ли обратный порядок сортировки')
    ):
        self.rows_per_page = rows_per_page
        self.page = page
        self.sort_by = sort_by
        self.descending = descending

    def dict(self):
        return vars(self)


class ListModel(Model):
    """
    Формат выдачи для всех списков объектов (multiple get)
    """
    rows_per_page: Optional[int]
    page: Optional[int]
    rows_number: Optional[int]
    data: List[ListElement]
    sort_by: str = 'uuid'
    descending: bool = False


class Named(IdMixin):
    name: str
