from typing import List, Optional

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
    directors: Optional[List[Named]] = Field(default_factory=list())
    actors: Optional[List[Named]] = Field(default_factory=list())
    writers: Optional[List[Named]] = Field(default_factory=list())


class FilmList(ListModel):
    data: List[FilmBase]


class GetMultiQueryParamFilms(GetMultiQueryParam):
    sort_by: str = Field('imdb_rating')
    descending: bool = Field(True)
