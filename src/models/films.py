from typing import List

from src.models.core import IdMixin, ListModel


class FilmBase(IdMixin):
    title: str


class FilmBare(FilmBase):
    pass


class FilmFull(FilmBare):
    pass


class FilmList(ListModel):
    data: List[FilmBase]
