from aioredis import Redis


async def clear_cache(redis_client: Redis):
    await redis_client.flushall()
