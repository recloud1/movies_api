import uuid
from typing import List, TypeVar, Optional

import orjson
from pydantic import BaseModel, validator, Field


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
    id: str = Field(..., alias='uuid')

    @validator('id')
    def ensure_uuid(cls, value):
        err = ValueError('Некорректный идентификатор')
        try:
            validated = uuid.UUID(value)
            if validated.version != 4:
                raise err
        except ValueError:
            raise err

        return value


class GetMultiQueryParam(Model):
    rows_per_page: int = Field(25, description='Количество объектов на одной странице')
    page: int = Field(1, description='Текущая страница')
    sort_by: str = Field('id', description='Поле сортировки результатов')
    descending: bool = Field(False, description='Использовать ли обратный порядок сортировки')


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
