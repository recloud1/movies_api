from typing import List

from models.core import ListModel, Named


class PersonBase(Named):
    pass


class PersonBare(PersonBase):
    pass


class PersonFull(PersonBase):
    pass


class PersonList(ListModel):
    data: List[PersonBare]
