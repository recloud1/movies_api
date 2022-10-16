import pytest_asyncio

from utils.elastic import init_elastic_data, clear_elastic_data


@pytest_asyncio.fixture(scope='session', autouse=True)
async def elastic_data(es_client):
    await init_elastic_data(es_client)
    yield
    await clear_elastic_data(es_client)
