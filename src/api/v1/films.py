from fastapi import APIRouter, Depends

from models.films import FilmList
from services.films import FilmElasticService, get_film_service

films = APIRouter()


@films.get('/', response_model=FilmList, summary='Получение списка фильмов', )
async def get_films(film_service: FilmElasticService = Depends(get_film_service)):
    pass


@films.get('/{film_id}')
async def get_film():
    pass
