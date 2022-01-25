from config import Settings, get_settings
from connections import redis_cache
from fastapi import APIRouter, Depends

router = APIRouter(
    tags=["status"],
)


@router.get("/")
async def pong(settings: Settings = Depends(get_settings)):
    """
    Return app settings

    """
    return {
        "message": "Hello World",
        "environment": settings.environment,
        "testing": settings.testing,
    }


@router.get("/react")
async def test_react():
    """
    Endpoint to test react

    """
    return {"message": "hello"}


@router.get("/redis{key}")
async def test_redis(key: str):
    """
    Endpoint to test react

    """
    value = await redis_cache.get(key)
    return {"message": value}


@router.put("/redis")
async def test_redis(key: str, value: str):
    """
    Endpoint to test react

    """
    await redis_cache.set(key, value)
    return {"message": f"Success, set {key}:{value}"}
