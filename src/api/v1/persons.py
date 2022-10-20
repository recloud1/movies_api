from typing import Optional

from fastapi import APIRouter, Depends, Path, Query

from models.core import GetMultiQueryParam
from models.params import Search, SearchValue
from models.persons import PersonBase, PersonList
from services.persons import PersonElasticService, get_person_service

persons = APIRouter()


@persons.get(
    '',
    response_model=PersonList,
    summary='Получение списка личностей',
    description='Список персоналий',
)
async def get_persons(
        person_service: PersonElasticService = Depends(get_person_service),
        query_params: GetMultiQueryParam = Depends(),
) -> PersonList:
    results, count = await person_service.get_multi(query_params=query_params)
    return PersonList(**query_params.dict(), rows_number=count, data=results)


@persons.get(
    '/search',
    response_model=PersonList,
    summary='Получение списка личностей',
    description='Список персоналий с возможность поиска',
)
async def get_persons_search(
        person_service: PersonElasticService = Depends(get_person_service),
        query_params: GetMultiQueryParam = Depends(),
        query: Optional[str] = Query(None, description='Поиск по персоналиям'),
) -> PersonList:
    results, count = await person_service.get_multi(
        query_params=query_params,
        search=Search(values=[SearchValue(field='name', value=query)]) if query else None
    )
    return PersonList(**query_params.dict(), rows_number=count, data=results)


@persons.get(
    '/{person_id}',
    response_model=PersonBase,
    summary='Получение информации о конкретной личности',
    description='Получить личность по ID',
)
async def get_person(
    person_id: str = Path(...),
    person_service: PersonElasticService = Depends(get_person_service),
) -> Optional[PersonBase]:
    result = await person_service.get(_id=person_id)
    return result
