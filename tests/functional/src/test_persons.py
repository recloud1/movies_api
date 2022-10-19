import pytest

from core.constants import RequestMethods, ApiRoutes
from testdata.persons import persons
from utils.requests import api_request, default_query_params


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
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params={**default_query_params, 'page[number]': 1},
    )
    assert len(data['data']) == default_query_params['page[size]'], 'Incorrect default number of persons per page'


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
    assert response.status == 422, 'Incorrect response on getting not existed page'


@pytest.mark.asyncio
async def test_get_persons_by_id(elastic_data, request_client):
    person_id = '6a0a479b-cfec-41ac-b520-41b2b007b611'
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        with_check=False,
        route_detail=person_id,
    )
    assert data['name'] == next(
        (person['name'] for person in persons if person['id'] == person_id), None
    ), 'Incorrect get person by id'


@pytest.mark.asyncio
async def test_search_person_by_name(elastic_data, request_client):
    person_name = 'Animation'
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params={'search': person_name},
        with_check=False,
    )
    assert data[0]['name'] == 'Animation', 'Incorrect person search by name'


@pytest.mark.asyncio
async def test_search_not_existed_person(elastic_data, request_client):
    person_name = 'No name'
    response, data = await api_request(
        request_client,
        RequestMethods.get,
        ApiRoutes.persons,
        query_params={'search': person_name},
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
