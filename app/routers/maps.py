from fastapi import APIRouter

from app.auth.repos import mapRepo

router = APIRouter(prefix="/map")


@router.get("/raw")
async def get_raw():
    return mapRepo.get_map()
