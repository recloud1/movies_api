from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.constants import ElasticIndexes
from db.elastic import get_elastic
from db.redis import get_redis
from models.genres import GenreBase
from services.core import ElasticServiceBase


class GenreElasticService(ElasticServiceBase):
    pass


@lru_cache
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreElasticService:
    return GenreElasticService(GenreBase, index=ElasticIndexes.genres, cache_service=redis, db_service=elastic)
