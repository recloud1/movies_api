import pytest

from core.constants import RequestMethods, ApiRoutes
from utils.requests import api_request


# не тест в обычном понимании - просто проверка запуска
@pytest.mark.asyncio
async def test_film_stub(request_client, elastic_data):
    response, data = await api_request(request_client, RequestMethods.get, ApiRoutes.films)

    assert response.status == 200
    assert len(data.get('data')) == 25
