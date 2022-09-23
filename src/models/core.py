import uuid
from typing import List, TypeVar

import orjson
from pydantic import BaseModel, validator


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
    id: str

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


class ListModel(Model):
    """
    Формат выдачи для всех списков объектов (multiple get)
    """
    rows_per_page: int | None
    page: int | None
    rows_number: int | None
    data: List[ListElement]
    sort_by: str = 'id'
    descending: bool = False


class Named(IdMixin):
    name: str
