import asyncio

from app.jobs.Drone import DronesFactory
from app.jobs.tools.MeasurmentHelper import measurments_to_points


class SwarmController:

    # TODO: add get_drones_positions() method
    def __init__(self, uris, point_cloud):
        self.point_cloud = point_cloud
        self.drones = DronesFactory(self.on_new_data).construct(uris)

    def get_drones_info(self):
        return [str(drone) for drone in self.drones]

    def get_drones_positions(self):
        positions = []
        for drone in self.drones:
            positions.append({drone.position})
        return positions

    def connect(self):
        for drone in self.drones:
            drone.connect()

    def on_new_data(self, timestamp, data, config):
        new_points = measurments_to_points(data["measurement"], data["pos"], timestamp)
        self.point_cloud.add(new_points)

    def _take_off_and_scan_around(self):
        for drone in self.drones:
            drone.take_off()
            drone.scan_around()
            drone.land(0)
            drone.disconnect()

    def take_off_and_scan_around(self):
        self._take_off_and_scan_around()

    def take_off_and_z_scan(self):
        for drone in self.drones:
            drone.take_off()
            drone.scan_z_shaped([2, 2, 0.2], 1, 1.0)
            drone.land(0)
            drone.disconnect()

    def _scan_vertical_object(self, height, width):
        drone = self.drones[0]
        drone.scan_z_shaped([0.3, 0.3, 0.2], 0.7, 1)

    async def swarm_set(self, drone):
        drone.take_off()
        drone.scan_around()
        drone.land(0)
        drone.disconnect()
