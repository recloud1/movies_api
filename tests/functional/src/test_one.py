import pytest

from core.settings import test_settings


@pytest.mark.asyncio
async def test_stub(es_client, request_client, redis_client):
    es_connected = await es_client.ping()
    redis_connected = await redis_client.ping()

    async with request_client.request(
            method='GET',
            url=f'http://{test_settings.api.host}:{test_settings.api.port}/api/docs'
    ) as response:
        api_status = response.status

    assert es_connected
    assert redis_connected
    assert api_status == 200
