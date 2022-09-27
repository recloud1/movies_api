from typing import Any, List

from models.core import Model


class FilterValue(Model):
    field: str
    value: Any


class Filters(Model):
    values: List[FilterValue]


class SearchValue(Model):
    field: str
    value: Any


class Search(Model):
    values: List[SearchValue]
