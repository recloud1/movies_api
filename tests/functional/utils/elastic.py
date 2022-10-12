from typing import List, Optional, Tuple

from elasticsearch import AsyncElasticsearch
from elasticsearch._async import helpers


async def create_elastic_index(
        adapter: AsyncElasticsearch,
        index_config: dict,
        name: str,
        with_ignore: bool = True
) -> None:
    ignore = 400 if with_ignore else None
    await adapter.indices.create(index=name, body=index_config, ignore=ignore)


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

    return await helpers.async_bulk(
        client=adapter,
        actions=data,
        index=index,
        doc_type='doc',
        stats_only=True,
        raise_on_error=raise_error
    )
