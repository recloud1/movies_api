from typing import Optional

from fastapi import APIRouter, Depends, Query, Path

from models.core import GetMultiQueryParam
from models.genres import GenreBase, GenreList
from models.params import SearchValue, Search
from services.genres import get_genre_service, GenreElasticService

genres = APIRouter()


@genres.get(
    '',
    response_model=GenreList,
    summary='Получение списка жанров',
    description='Список жанров с возможность поиска и сортировки',
)
async def get_genres(
        genre_service: GenreElasticService = Depends(get_genre_service),
        query_params: GetMultiQueryParam = Depends(),
        search: Optional[str] = Query(None, description='Поиск по жанрам'),
) -> GenreList:
    results, count = await genre_service.get_multi(
        query_params=query_params,
        search=Search(values=[SearchValue(field='name', value=search)]) if search else None
    )
    return GenreList(**query_params.dict(), rows_number=count, data=results)


@genres.get(
    '/{genre_id}',
    response_model=GenreBase,
    summary='Получение информации о конкретном жанре',
    description='Получить жанр по его ID',
)
async def get_genre(
    genre_id: str = Path(...),
    genre_service: GenreElasticService = Depends(get_genre_service),
) -> Optional[GenreBase]:
    result = await genre_service.get(_id=genre_id)
    return result
