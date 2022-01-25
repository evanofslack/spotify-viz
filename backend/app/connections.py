from typing import Optional

import aioredis

from config import get_settings

settings = get_settings()


class RedisCache:
    def __init__(self):
        self.redis_cache: Optional[aioredis.Redis] = None

    async def init_cache(self):
        self.redis_cache = await aioredis.from_url(settings.redis_url, encoding="utf-8")

    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)

    async def set(self, key, value):
        return await self.redis_cache.set(key, value)

    async def get(self, key):
        return await self.redis_cache.get(key)

    async def close(self):
        self.redis_cache.close()
        await self.redis_cache.wait_closed()


redis_cache = RedisCache()
