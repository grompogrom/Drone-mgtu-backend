from fastapi import APIRouter, BackgroundTasks
import json


from app.auth.repos import mapRepo, dronesRepo
from app.jobs.tools.Status import Status

router = APIRouter(prefix="/control")


@router.get("/")
async def read_control():
    return {"Hello": "Control"}


@router.get("/charge/")
async def get_battery_charge():
    # todo
    return [{"address": "e3e4e4e4e4e4", "charge": 3.56}, {"address": "e3e4e4e4e4e5", "charge": 4.06}]


@router.get("/map/")
async def get_map():
    mapRepo.point_cloud.save()
    data = {
        "status": "good",
        "data": mapRepo.get_map()
    }
    return data


@router.get("/status/")
async def get_status():
    status = dronesRepo.get_status()
    return str(status)

@router.post(
    "/connect_drones",
    responses={403: {"description": "Operation forbidden"},
               200: {"description": "Success"}},
)
async def connect_drones(background_tasks: BackgroundTasks):
    background_tasks.add_task(dronesRepo.connect)
    return True


@router.post(
    "/start_scan",
    responses={403: {"description": "Operation forbidden"}, 200: {"description": "Success"}},
)
async def start_scan(background_tasks: BackgroundTasks):
    mapRepo.clear_map()
    background_tasks.add_task(dronesRepo.start_scan)
    return True
