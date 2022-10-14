import aioredis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from api.v1.films import films
from api.v1.genres import genres
from api.v1.persons import persons
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
    description='Информация о фильмах, жанрах и людях, участвовавших в создании произведения',
    docs_url='/api/v1/docs',
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
    allow_credentials=True,
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


app.include_router(films, prefix='/v1/films', tags=['Films'], responses=default_errors)
app.include_router(genres, prefix='/v1/genres', tags=['Genres'], responses=default_errors)
app.include_router(persons, prefix='/v1/persons', tags=['Persons'], responses=default_errors)