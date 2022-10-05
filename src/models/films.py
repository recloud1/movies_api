from typing import List, Optional

from fastapi import Query
from pydantic import Field

from models.core import GetMultiQueryParam
from src.models.core import IdMixin, ListModel, Named


class FilmBase(IdMixin):
    title: str
    imdb_rating: Optional[float] = Field(None)
    file_path: Optional[str] = Field(None)


class FilmBare(FilmBase):
    description: Optional[str] = Field(None)


class FilmFull(FilmBare):
    directors: Optional[List[Named]] = Field(default=list())
    actors: Optional[List[Named]] = Field(default=list())
    writers: Optional[List[Named]] = Field(default=list())
    genre: Optional[List[str]] = Field(default=list(), alias='genres')


class FilmList(ListModel):
    data: List[FilmBase]


class GetMultiQueryParamFilms(GetMultiQueryParam):
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
                ge=1,
                le=100,
                alias='page[size]',
                description='Количество объектов на одной странице'
            ),
            sort_by: str = Query(
                default='imdb_rating',
                description='Поле сортировки результатов',
                alias='sort'
            ),
            descending: bool = Query(
                default=True,
                description='Использовать ли обратный порядок сортировки'
            )
    ):
        super().__init__(page=page, rows_per_page=rows_per_page)
        self.sort_by = sort_by
        self.descending = descending
