from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def get_overview():
    pass
