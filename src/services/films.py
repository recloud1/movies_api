from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.constants import ElasticIndexes
from db.elastic import get_elastic
from db.redis import RedisCache, get_redis
from models.films import FilmBase
from services.core import CachedElasticPaginated


class FilmElasticService(CachedElasticPaginated):
    pass


@lru_cache
def get_film_service(
        redis: RedisCache = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmElasticService:
    return FilmElasticService(
        model=FilmBase,
        index=ElasticIndexes.movies,
        cache_service=redis,
        db_service=elastic,
        expired_data_seconds=600
    )
