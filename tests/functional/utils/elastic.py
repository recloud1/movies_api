import asyncio
from pathlib import Path
from typing import List, Optional, Tuple

from elasticsearch import AsyncElasticsearch
from elasticsearch._async import helpers

from testdata.common import testdata
from utils.json_reader import JsonReader

ES_INDEXES = [
    'movies',
    'persons',
    'genres'
]


async def create_elastic_index(
        adapter: AsyncElasticsearch,
        index_config: dict,
        name: str,
        with_ignore: bool = True
) -> None:
    ignore = 400 if with_ignore else None
    return await adapter.indices.create(index=name, body=index_config, ignore=ignore)


async def elastic_bulk_load(
        adapter: AsyncElasticsearch,
        data: List[dict],
        index: str,
        create_index: bool = False,
        index_config: Optional[dict] = None,
        raise_error: bool = False
) -> Tuple[int, int]:
    if create_index and index_config:
        await create_elastic_index(adapter, index_config, index)

    data = [{'_index': index, '_id': item.get('id'), **item} for item in data]

    return await helpers.async_bulk(
        client=adapter,
        actions=data,
        index=index,
        stats_only=True,
        raise_on_error=raise_error
    )


async def init_elastic_data(es_client: AsyncElasticsearch):
    results = []
    for index in ES_INDEXES:
        schema_file = Path(__file__).resolve().parent.parent / f'testdata/schemas/{index}.json'
        index_config = JsonReader(schema_file).read()

        await create_elastic_index(es_client, index_config, index)
        results.append(await elastic_bulk_load(es_client, testdata.get(index), index, raise_error=True))

    return results


async def clear_elastic_data(es_client: AsyncElasticsearch):
    for index in ES_INDEXES:
        await es_client.indices.delete(index=index)
