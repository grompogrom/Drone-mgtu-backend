from app.jobs.PointClout import PointCloud
from app.jobs.SwarmController import SwarmController
from app.jobs.tools.SaveDataHelper import save_points_to_file
from app.jobs.tools.Status import Status


class DronesRepository:
    def __init__(self, point_cloud=PointCloud(save_points_to_file)):
        self._status = Status.DISCONNECTED
        self.uris = ["radio://0/80/2M/E7E7E7E7E7"]
        self.point_cloud = point_cloud
        self.swarm_controller = SwarmController(self.uris, self.point_cloud)

    def connect(self):
        if self._status != Status.DISCONNECTED:
            return
        try:
            self.swarm_controller.connect()
            self._status = Status.CONNECTED
        except Exception:
            self._status = Status.DISCONNECTED

    def get_drones_info(self):
        return self.swarm_controller.get_drones_info()

    def get_status(self):
        return self._status.value

    def start_scan(self):
        if self.swarm_controller is None:
            return
        if self._status != Status.CONNECTED:
            return
        self._status = Status.FLYING
        try:
            self.swarm_controller.take_off_and_scan_around()
        except Exception as e:
            print(e.with_traceback())
            self._status = Status.DISCONNECTED
        finally:
            self._status = Status.DISCONNECTED

    def start_demo_three(self):
        pass

    def pause(self):
        pass

    def end_of_session(self):
        self._status = Status.DISCONNECTED
