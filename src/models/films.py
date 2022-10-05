from typing import List, Optional

from pydantic import Field

from models.core import GetMultiQueryParam, Named, IdMixin, ListModel


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
    sort_by: str = Field('imdb_rating')
    descending: bool = Field(True)
