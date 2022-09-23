from fastapi import APIRouter, Depends

from models.persons import PersonList
from services.genres import GenreElasticService
from services.persons import get_person_service

persons = APIRouter()


@persons.get('/', response_model=PersonList, summary='Получение списка личностей')
async def get_persons(genre_service: GenreElasticService = Depends(get_person_service)):
    pass


@persons.get('/{person_id}')
async def get_person():
    pass
