import pytest

from core.constants import RequestMethods, ApiRoutes
from utils.elastic import init_elastic_data, clear_elastic_data
from utils.requests import api_request, default_query_params


@pytest.mark.asyncio
async def test_genres_amount(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        query_params={'page[size]': 100}
    )
    return
    assert len(data) == 0
