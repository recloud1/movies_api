import pytest
from elasticsearch import AsyncElasticsearch

from utils.elastic import init_elastic_data, clear_elastic_data


# @pytest.fixture(scope='session')
# async def es_data(es_client: AsyncElasticsearch):
#     results = await init_elastic_data(es_client)
#
#     yield results
#
#     await clear_elastic_data(es_client)
