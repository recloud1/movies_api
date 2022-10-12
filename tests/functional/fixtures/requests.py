from typing import Tuple

import pytest

from core.settings import test_settings


@pytest.fixture
async def api_request(request_client, method, route, query_params) -> Tuple[dict, dict, int]:
    url = f'{test_settings.api.host}:{test_settings.api.port}/api/v1/{route}'
    request_params = {
        'method': method,
        'url': url,
        'params': query_params
    }

    async with request_client.request(**request_params) as response:
        body: dict = await response.json()
        header: dict = dict(response.headers)
        status: int = response.status

    return body, header, status
