from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.constants import ElasticIndexes
from db.elastic import get_elastic
from db.redis import get_redis, RedisCache
from models.genres import GenreBase
from services.core import CachedElasticPaginated


class GenreElasticService(CachedElasticPaginated):
    pass


@lru_cache
def get_genre_service(
        redis: RedisCache = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreElasticService:
    return GenreElasticService(
        model=GenreBase,
        index=ElasticIndexes.genres,
        cache_service=redis,
        db_service=elastic,
        expired_data_seconds=300
    )
