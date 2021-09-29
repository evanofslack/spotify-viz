from fastapi import APIRouter, Depends

from config import get_settings, Settings


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
        "testing": settings.testing
    }


@router.get("/react")
async def test_react():
    """
    Endpoint to test react 

    """
    return {"message": "hello"}
