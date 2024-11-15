from http import HTTPStatus
from typing import Any, List, Optional

import pytest
from pydantic import BaseModel
from testdata.films import films
from utils.redis import clear_cache
from utils.requests import api_request, default_query_params

from core.constants import ApiRoutes, RequestMethods


class DataTestExpected(BaseModel):
    status: Optional[int]
    value: Optional[Any]


class DataTest(BaseModel):
    value: Any
    expected: DataTestExpected
    description: Optional[str]
    params: Optional[Any]


get_by_id_data: List[DataTest] = [
    DataTest(
        value='e7e6d147-cc10-406c-a7a2-5e0be2231327',
        expected=DataTestExpected(status=HTTPStatus.OK, value='e7e6d147-cc10-406c-a7a2-5e0be2231327'),
        description='Фильм найден без кэша',
        params=False
    ),
    DataTest(
        value='e7e6d147-cc10-406c-a7a2-5e0be2231327',
        expected=DataTestExpected(status=HTTPStatus.OK, value='e7e6d147-cc10-406c-a7a2-5e0be2231327'),
        description='Фильм найден с кэшем',
        params=True
    ),
    DataTest(
        value='some_id',
        expected=DataTestExpected(status=HTTPStatus.NOT_FOUND, value=None),
        description='Фильм не найден'
    )
]


@pytest.mark.asyncio
@pytest.mark.parametrize('test_data', get_by_id_data)
async def test_get_film_by_id(request_client, redis_client, elastic_data, test_data):
    if test_data.params:
        await clear_cache(redis_client)

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.films,
        route_detail=test_data.value,
        with_check=False
    )

    assert response.status == test_data.expected.status
    assert data.get('id') == test_data.expected.value


@pytest.mark.asyncio
async def test_get_all_films(request_client, elastic_data):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.films,
        with_check=False,
        query_params={**default_query_params, 'page[size]': 0}
    )

    assert len(data.get('data')) == len(films)


wrong_query_params: List[DataTest] = [
    DataTest(
        value={**default_query_params, 'page[size]': -1},
        expected=DataTestExpected(status=HTTPStatus.UNPROCESSABLE_ENTITY),
        description='Нарушение количества объектов на странице'
    ),
    DataTest(
        value={**default_query_params, 'page[size]': 101},
        expected=DataTestExpected(status=HTTPStatus.UNPROCESSABLE_ENTITY),
        description='Нарушение количества объектов на странице'
    ),

    DataTest(
        value={**default_query_params, 'page[number]': 0},
        expected=DataTestExpected(status=HTTPStatus.UNPROCESSABLE_ENTITY),
        description='Нарушение номера страницы'
    ),

    DataTest(
        value={**default_query_params, 'page[number]': -1},
        expected=DataTestExpected(status=HTTPStatus.UNPROCESSABLE_ENTITY),
        description='Нарушение номера страницы'
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize('query_params', wrong_query_params)
async def test_get_films_with_wrong_query_params_failed(request_client, elastic_data, query_params):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.films,
        with_check=False,
        query_params=query_params.value
    )

    assert response.status == query_params.expected.status


search_test_data = [
    DataTest(
        value='Bucky Larson',
        expected=DataTestExpected(
            status=HTTPStatus.OK,
            value={'count': 1, 'id': '935e418d-09f3-4de4-8ce3-c31f31580b12'}
        ),
        params=False,
        description='Удачный поиск по названию'
    ),
    DataTest(
        value='Some nothing name',
        expected=DataTestExpected(
            status=HTTPStatus.OK,
            value={'count': 0, 'id': None}
        ),
        params=False,
        description='Безрезультатный поиск'
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize('search_data', search_test_data)
async def test_get_films_by_search(request_client, redis_client, elastic_data, search_data):
    if search_data.params:
        await clear_cache(redis_client)
    index_of_film_in_result = search_data.expected.value.get('count') - 1

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.films,
        route_detail='search',
        with_check=False,
        query_params={**default_query_params, 'query': search_data.value}
    )
    data = data.get('data')
    objects_count = len(data)

    assert response.status == search_data.expected.status
    assert objects_count == search_data.expected.value.get('count')

    if objects_count > 0:
        assert data[index_of_film_in_result].get('id') == search_data.expected.value.get('id')

