from typing import Optional

from fastapi import APIRouter, Depends, Path, Query

from models.films import FilmFull, FilmList, GetMultiQueryParamFilms
from models.params import Filters, FilterValue, Search, SearchValue
from services.films import FilmElasticService, get_film_service

films = APIRouter()


@films.get(
    '',
    response_model=FilmList,
    summary='Получение списка кинопроизведений',
    description='Список кинопроизведений с возможность поиска и фильтрации'
)
async def get_films(
        film_service: FilmElasticService = Depends(get_film_service),
        query_params: GetMultiQueryParamFilms = Depends(),
        genre: Optional[str] = Query(None, description='Фильтрация фильмов по наименованию жанра'),
        search: Optional[str] = Query(None, description='Поиск по кинопроизведениям')
) -> FilmList:
    results, count = await film_service.get_multi(
        query_params=query_params,
        filters=Filters(values=[FilterValue(field='genre', value=genre)]) if genre else None,
        search=Search(values=[SearchValue(field='title', value=search)]) if search else None
    )

    return FilmList(**query_params.dict(), rows_number=count, data=results)


@films.get(
    '/{film_id}',
    response_model=FilmFull,
    summary='Получение информации о конкретном фильме',
    description='Получение полной информации о конкретном фильме'
)
async def get_film(
        film_id: str = Path(...),
        film_service: FilmElasticService = Depends(get_film_service)
) -> Optional[FilmFull]:
    result = await film_service.get(_id=film_id, model=FilmFull)

    return result
