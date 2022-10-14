from typing import Tuple

from aiohttp import ClientResponse

from core.constants import RequestMethods, ApiRoutes
from core.settings import test_settings


async def api_request(
        request_client,
        method: RequestMethods,
        route: ApiRoutes,
        route_detail: str = '',
        query_params=None,
        with_check: bool = True
) -> Tuple[ClientResponse, dict]:
    async with request_client.request(
            method=method,
            url=f'http://{test_settings.api.host}:{test_settings.api.port}/v1/{route}/{route_detail}',
            params=query_params
    ) as response:

        if with_check:
            assert response.status == 200

        data = await response.json()

        return response, data
