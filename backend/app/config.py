import logging
import os
from functools import lru_cache

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT")
    testing: bool = os.getenv("TESTING")
    redis_url: str = os.getenv("REDIS_URL")
    home_url: str = os.getenv("HOME_URL")


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
