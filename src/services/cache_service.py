import json
from abc import ABC, abstractmethod
from typing import Any, List

from aioredis import Redis

EXPIRE = 60 * 5


class CacheService(ABC):

    @abstractmethod
    def build_key(self, api_name: str, params: List = None) -> str:
        pass

    @abstractmethod
    async def set_value(self, key: str, data: Any) -> Any:
        pass

    @abstractmethod
    async def get_value(self, api_name: str) -> Any:
        pass


class RedisService(CacheService):

    def __init__(self, redis: Redis):
        self._redis = redis

    def build_key(self, api_name: str, params: List = None) -> str:
        if params is None:
            params = list()
        params_to_str = ','.join([str(elem) for elem in params])
        return f'{api_name}:{params_to_str}'

    async def set_value(self, key: str, data: Any):
        json_data = json.dumps(data)
        return await self._redis.set(
            key=key,
            value=json_data,
            expire=EXPIRE,
        )

    async def get_value(self, api_name: str) -> Any:
        if cache := await self._redis.get(api_name):
            return json.loads(cache)
        return None
