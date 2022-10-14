import asyncio

import aiohttp
import aioredis
import pytest
import pytest_asyncio
from core.settings import test_settings
from elasticsearch import AsyncElasticsearch


# Переопределение event_loop - не нужно использовать как фикстуру напрямую
@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope='session')
async def es_client():
    connect_data = {
        'scheme': 'http',
        'host': test_settings.elastic.host,
        'port': test_settings.elastic.port,
        'use_ssl': False,
        'validate_cert': False
    }
    adapter = AsyncElasticsearch([connect_data])

    yield adapter

    await adapter.close()


@pytest_asyncio.fixture(scope='session')
async def request_client():
    session = aiohttp.ClientSession()

    yield session

    await session.close()


@pytest_asyncio.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis(
        address=(test_settings.redis.host, test_settings.redis.port),
        password=test_settings.redis.password,
    )
    await redis.flushall()

    yield redis

    redis.close()
    await redis.wait_closed()
