from typing import List, Optional

from pydantic import Field

from core.constants import PersonRoles
from models.core import ListModel, Named


class PersonBase(Named):
    name: str = Field(..., alias='full_name')
    role: Optional[PersonRoles]


class PersonFull(PersonBase):
    film_ids: List[str]


class PersonList(ListModel):
    data: List[PersonBase]
