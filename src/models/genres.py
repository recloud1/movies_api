from typing import List, Optional

from pydantic import Field

from models.core import ListModel, Named


class GenreBase(Named):
    description: Optional[str] = Field(None)


class GenreList(ListModel):
    data: List[Named]
