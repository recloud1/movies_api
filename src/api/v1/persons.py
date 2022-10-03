from typing import Optional

from fastapi import APIRouter, Depends, Query, Path

from models.core import GetMultiQueryParam
from models.params import Search, SearchValue
from models.persons import PersonList, PersonBase
from services.persons import get_person_service, PersonElasticService

persons = APIRouter()


@persons.get(
    '',
    response_model=PersonList,
    summary='Получение списка личностей',
    description='Список персоналий с возможность поиска и сортировки',
)
async def get_persons(
        person_service: PersonElasticService = Depends(get_person_service),
        query_params: GetMultiQueryParam = Depends(),
        search: Optional[str] = Query(None, description='Поиск по персоналиям'),
) -> PersonList:
    results, count = await person_service.get_multi(
        query_params=query_params,
        search=Search(values=[SearchValue(field='name', value=search)]) if search else None
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
    result = await person_service.get(_id=person_id, model=PersonBase)
    return result
