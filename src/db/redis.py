import json
from functools import lru_cache
from json import JSONEncoder
from typing import Any, Optional
from uuid import UUID

import orjson
from aioredis import Redis

redis: Optional[Redis] = None

old_default = JSONEncoder.default


def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default


class RedisCache:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    """

    def __init__(self, storage: Redis):
        self.storage = storage

    async def set(self, key: str, value: Any, expire_time_seconds: int) -> None:
        """Сохранение данных под определенным ключом"""
        value = self._encode_json(value)
        await self.storage.setex(key=key, value=value, seconds=expire_time_seconds)
        await self.storage.set(key=key, value=value)

    async def get(self, key: str, default=None) -> Any:
        """Получить данные по определённому ключу"""
        result = await self.storage.get(key=key)
        if not result:
            return default

        result = self._decode_json(result)

        return result

    def _decode_json(self, val: Any) -> Any:
        """
        Распаковка данных из кэша

        :param val: данные
        :return: распакованные данные
        """
        return orjson.loads(val)

    def _encode_json(self, val: Any) -> str:
        """
        Запаковка данных для кэша

        :param val: данные
        :return: запакованные данные
        """
        return json.dumps(val)


@lru_cache
def get_redis() -> RedisCache:
    return RedisCache(storage=redis)
