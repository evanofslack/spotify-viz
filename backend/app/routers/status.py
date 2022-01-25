from config import Settings, get_settings
from connections import redis_cache
from fastapi import APIRouter, Depends

router = APIRouter(
    tags=["playlists"],
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


@router.get("/redis")
async def test_react():
    """
    Endpoint to test react

    """
    await redis_cache.set("test", "hello redis!")
    value = await redis_cache.get("test")
    return {"message": value}
