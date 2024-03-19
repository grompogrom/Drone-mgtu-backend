from app.jobs.DronesRepository import DronesRepository
from app.jobs.PointClout import PointCloud
from app.jobs.tools.SaveDataHelper import save_points_to_file
from app.map.MapRepository import MapRepository

pointCloud = PointCloud(save_points_to_file)
dronesRepo = DronesRepository(pointCloud)
mapRepo = MapRepository(pointCloud)