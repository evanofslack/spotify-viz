from typing import Optional

import aioredis

from config import get_settings

settings = get_settings()


class RedisCache:
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None

    async def init_cache(self):
        self.redis = await aioredis.from_url(settings.redis_url, encoding="utf-8")

    async def keys(self, pattern):
        return await self.redis.keys(pattern)

    async def set(self, key, value):
        return await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def exists(self, key):
        return await self.redis.exists(key)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()

    async def hset(self, hash_name: str, key, value):
        return await self.redis.hset(hash_name, key, value)


redis_cache = RedisCache()
