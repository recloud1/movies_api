from http import HTTPStatus

import pytest
from testdata.persons import persons
from utils.requests import api_request, default_query_params

from core.constants import ApiRoutes, RequestMethods


@pytest.mark.asyncio
async def test_persons_amount(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params={**default_query_params, 'page[size]': 0},
    )

    assert len(data['data']) == len(persons), 'Incorrect number of persons'


@pytest.mark.asyncio
async def test_persons_page_size(elastic_data, request_client):
    query_params = {**default_query_params, 'page[size]': 10}

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params=query_params
    )

    assert len(data['data']) == query_params['page[size]'], 'Incorrect default number of persons per page'


@pytest.mark.asyncio
async def test_persons_not_existed_page(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params={**default_query_params, 'page[number]': 100},
    )

    assert len(data['data']) == 0, 'Incorrect response on getting not existed page'


@pytest.mark.asyncio
async def test_persons_incorrect_page_number(elastic_data, request_client):
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        with_check=False,
        query_params={**default_query_params, 'page[number]': -1},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY, 'Incorrect response on getting not existed page'


@pytest.mark.asyncio
async def test_get_persons_by_id(elastic_data, request_client):
    person_id = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        route_detail=person_id,
        with_check=False,
    )

    assert data['id'] == person_id, 'Incorrect person search by name'


@pytest.mark.asyncio
async def test_search_person_by_name(elastic_data, request_client):
    person_name = 'Richard Marquand'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        route_detail='search',
        query_params={'query': person_name},
        with_check=False,
    )

    assert data.get('data')[0]['full_name'] == person_name, 'Incorrect person search by name'


@pytest.mark.asyncio
async def test_search_not_existed_person(elastic_data, request_client):
    person_name = 'No name'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        route_detail='search',
        query_params={'query': person_name},
        with_check=False,
    )

    assert len(data['data']) == 0, 'Incorrect search of not existed person name'


@pytest.mark.asyncio
async def test_get_not_existed_id(elastic_data, request_client):
    person_id = '123456qwerty'

    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        route_detail=person_id,
        with_check=False,
    )

    assert data['detail'] == f'Объект с идентификатором {person_id} не найден', 'Incorrect get person by not existed id'
