import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.films import films
from api.v1.genres import genres
from core.config import envs
from db import elastic, redis

default_errors = {
    401: {'description': 'Unauthorized'},
    403: {'description': 'No permission'},
    404: {'description': 'Object not found'},
    409: {'description': 'Collision occurred. Entity already exists'},
    410: {'description': 'Already Expired'}
}

app = FastAPI(
    title=envs.project.name,
    docs_url='/api/docs',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse
)


@app.on_event('startup')
async def on_startup():
    redis.redis = await aioredis.create_redis_pool(
        (envs.redis.host, envs.redis.port),
        password=envs.redis.password,
        minsize=envs.redis.pool_minsize,
        maxsize=envs.redis.pool_maxsize
    )

    elastic.es = AsyncElasticsearch(hosts=[f'{envs.elastic.host}:{envs.elastic.port}'])


@app.on_event('shutdown')
async def on_shutdown():
    await redis.redis.close()
    await elastic.es.close()

app.include_router(films, prefix='/films/v1', tags=['Films'], responses=default_errors)
app.include_router(genres, prefix='/films/v1', tags=['Films'], responses=default_errors)
app.include_router(persons, prefix='/films/v1', tags=['Films'], responses=default_errors)
