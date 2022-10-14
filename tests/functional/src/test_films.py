import pytest

from core.constants import RequestMethods, ApiRoutes
from utils.elastic import init_elastic_data, clear_elastic_data
from utils.requests import api_request


# не тест в обычном понимании - просто проверка запуска
@pytest.mark.asyncio
async def test_film_stub(es_client, request_client, redis_client):
    await init_elastic_data(es_client)

    response, data = await api_request(request_client, RequestMethods.get, ApiRoutes.films)

    assert response.status == 200
    assert len(data.get('data')) == 25

    await clear_elastic_data(es_client)
