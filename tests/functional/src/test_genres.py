from http import HTTPStatus

import pytest
from testdata.genres import genres
from utils.requests import api_request, default_query_params

from core.constants import ApiRoutes, RequestMethods


@pytest.mark.asyncio
async def test_genres_amount(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        query_params={**default_query_params, 'page[size]': 0},
    )

    assert len(data['data']) == len(genres), 'Incorrect number of genres'


@pytest.mark.asyncio
async def test_genres_page_size(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        query_params={**default_query_params, 'page[number]': 1},
    )

    assert len(data['data']) == default_query_params['page[size]'], 'Incorrect default number of genres per page'


@pytest.mark.asyncio
async def test_genres_not_existed_page(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        query_params={**default_query_params, 'page[number]': 100},
    )

    assert len(data['data']) == 0, 'Incorrect response on getting not existed page'


@pytest.mark.asyncio
async def test_genres_incorrect_page_number(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        with_check=False,
        query_params={**default_query_params, 'page[number]': -1},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Incorrect response on getting not existed page'


@pytest.mark.asyncio
async def test_get_genre_by_id(elastic_data, request_client):
    genre_id = '6a0a479b-cfec-41ac-b520-41b2b007b611'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        with_check=False,
        route_detail=genre_id,
    )

    assert data['id'] == genre_id


@pytest.mark.asyncio
async def test_search_genre_by_name(elastic_data, request_client):
    genre_name = 'Animation'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        route_detail='search',
        query_params={'query': genre_name},
        with_check=False,
    )

    assert data.get('data')[0]['name'] == 'Animation', 'Incorrect genre search by name'


@pytest.mark.asyncio
async def test_search_not_existed_genre(elastic_data, request_client):
    genre_name = 'No name'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        route_detail='search',
        query_params={'query': genre_name},
        with_check=False
    )

    assert len(data['data']) == 0, 'Incorrect search of not existed genre name'


@pytest.mark.asyncio
async def test_get_not_existed_id(elastic_data, request_client):
    genre_id = '123456qwerty'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.genres,
        route_detail=genre_id,
        with_check=False,
    )

    assert data['detail'] == f'Объект с идентификатором {genre_id} не найден', 'Incorrect get genre by not existed id'



