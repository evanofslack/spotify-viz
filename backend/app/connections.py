from typing import Optional

import aioredis

from config import get_settings

settings = get_settings()


class RedisCache:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def init_cache(self):
        self.redis = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )

    async def keys(self, pattern):
        return await self.redis.keys(pattern)

    async def set(self, key, value):
        return await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def exists(self, key):
        return await self.redis.exists(key)

    async def hset(self, hash_name: str, key, value):
        return await self.redis.hset(hash_name, key, value)

    async def hget(self, hash_name: str, key):
        return await self.redis.hget(hash_name, key)

    async def hmset(self, hash_name: str, map: dict):
        return await self.redis.hmset(hash_name, map)

    async def hgetall(self, hash_name: str):
        return await self.redis.hgetall(hash_name)

    async def close(self):
        await self.redis.close()
        await self.redis.wait_closed()


redis_cache = RedisCache()
