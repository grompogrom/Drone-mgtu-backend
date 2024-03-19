from fastapi import APIRouter

from app.auth.repos import dronesRepo

router = APIRouter(prefix="/stats")


@router.get("/")
async def get_status():
    return {"status": dronesRepo.get_status()}


@router.get("/drones")
async def get_drones_info():
    return dronesRepo.get_drones_info()


@router.get("/traces")
async def get_stats():
    return [
        {
            "drone_id": "1",
            "trace": [[0, 1, 2], [1, 1, 2]]
         }]
