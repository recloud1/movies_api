from functools import lru_cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.constants import ElasticIndexes
from db.elastic import get_elastic
from db.redis import get_redis, RedisCache
from models.persons import PersonBase
from services.core import CachedElasticPaginated


class PersonElasticService(CachedElasticPaginated):
    pass


@lru_cache
def get_person_service(
        redis: RedisCache = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonElasticService:
    return PersonElasticService(
        model=PersonBase,
        index=ElasticIndexes.persons,
        cache_service=redis,
        db_service=elastic,
        expired_data_seconds=300
    )
