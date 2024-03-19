from fastapi import APIRouter

from app.auth.repos import dronesRepo

router = APIRouter(prefix="/settings")


@router.post("/add_drones")
async def add_drone(drones: list[str]):
    dronesRepo.add_drones(drones)
    return {"status": "ok"}
