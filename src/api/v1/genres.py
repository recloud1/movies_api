from fastapi import APIRouter, Depends

from models.genres import GenreList
from services.genres import get_genre_service, GenreElasticService

genres = APIRouter()


@genres.get(
    '/',
    response_model=GenreList,
    summary='Получение списка жанров',
)
async def get_genres(
        genre_service: GenreElasticService = Depends(get_genre_service)):
    pass


@genres.get('/{genre_id}')
async def get_genre():
    pass
