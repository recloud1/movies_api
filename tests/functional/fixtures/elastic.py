from typing import List

from elasticsearch import AsyncElasticsearch
import pytest

from utils.elastic import elastic_bulk_load


@pytest.fixture
async def es_write_data(es_client: AsyncElasticsearch, data: List[dict], index: str):
    return await elastic_bulk_load(es_client, data, index)
