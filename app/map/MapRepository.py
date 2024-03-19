from app.jobs.PointClout import PointCloud
from app.jobs.tools.SaveDataHelper import save_points_to_file


class MapRepository:
    def __init__(self, point_cloud = PointCloud(save_points_to_file)):
        self.point_cloud = point_cloud
        pass

    def get_map(self):
        return self.point_cloud.get_points()

    def clear_map(self):
        self.point_cloud.clear_map()

    def get_map_front(self):
        return self.point_cloud.get_filtered_points({"front"})