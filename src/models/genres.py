from typing import List

from models.core import ListModel, Named


class GenreBase(Named):
    pass


class GenreBaseBare(GenreBase):
    pass


class GenreFull(GenreBaseBare):
    pass


class GenreList(ListModel):
    data: List[GenreBaseBare]
