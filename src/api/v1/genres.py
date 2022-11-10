from typing import Optional

from fastapi import APIRouter, Depends, Path, Query

from core.constants import ROLES
from dependencies.auth import user_has_role
from models.auth import UserInfoJWT
from models.core import GetMultiQueryParam
from models.genres import GenreBase, GenreList
from models.params import Search, SearchValue
from services.genres import GenreElasticService, get_genre_service

genres = APIRouter()


@genres.get(
    '',
    response_model=GenreList,
    summary='Получение списка жанров',
    description='Список жанров с возможность',
)
async def get_genres(
        genre_service: GenreElasticService = Depends(get_genre_service),
        query_params: GetMultiQueryParam = Depends(),
        author: UserInfoJWT = Depends(user_has_role(ROLES.user)),
) -> GenreList:
    results, count = await genre_service.get_multi(query_params=query_params)
    return GenreList(**query_params.dict(), rows_number=count, data=results)


@genres.get(
    '/search',
    response_model=GenreList,
    summary='Получение списка жанров',
    description='Список жанров с возможность поиска и сортировки',
)
async def get_genres_search(
        genre_service: GenreElasticService = Depends(get_genre_service),
        query_params: GetMultiQueryParam = Depends(),
        query: Optional[str] = Query(None, description='Поиск по жанрам'),
        author: UserInfoJWT = Depends(user_has_role(ROLES.user)),
) -> GenreList:
    results, count = await genre_service.get_multi(
        query_params=query_params,
        search=Search(values=[SearchValue(field='name', value=query)]) if query else None
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
    author: UserInfoJWT = Depends(user_has_role(ROLES.user)),
) -> Optional[GenreBase]:
    result = await genre_service.get(_id=genre_id)
    return result
