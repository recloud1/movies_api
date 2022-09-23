from functools import lru_cache

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from core.constants import ElasticIndexes
from db.elastic import get_elastic
from db.redis import get_redis
from models.persons import PersonBase
from services.core import ElasticServiceBase
from services.genres import GenreElasticService


class PersonElasticService(ElasticServiceBase):
    pass


@lru_cache
def get_person_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreElasticService:
    return GenreElasticService(
        PersonBase,
        index=ElasticIndexes.persons,
        cache_service=redis,
        db_service=elastic
    )
