import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils.callbacks import Caller

from app.jobs.Loger import Logger
from app.jobs.MotionCommander import MotionCommander
from app.jobs.config.scaning import VERTICAL_DELTA, SCANNING_GOTO_VELOCITY, ROTATION_VELOCITY as ROTATION_SCAN_VELOCITY


class Drone:
    def __init__(self, drone_uri, meas_listener=None):
        cflib.crtp.init_drivers()
        self.uri = drone_uri
        self.scf = SyncCrazyflie(drone_uri)
        self.commander = MotionCommander(self.scf.cf)
        self.on_data_received = Caller()
        self.logger = None
        self.status = "undefined"

        if meas_listener is not None:
            self.on_data_received.add_callback(meas_listener)

        self.position = []
        self.battery_state = {}

    def __str__(self):
        return {
            "id": 0,
            "address": self.uri,
            "battery": self.battery_state,
            "location": self.position,
            "status": self.status
        }

    def connect(self):
        self.scf.open_link()
        self._init_logger()

    def take_off(self):
        self.commander.take_off()

    def land(self, landing_height):
        self.commander.land(landing_height)

    def start_logging(self):
        self.logger.start_logging()

    def stop_loging(self):
        self.logger.stop_loging()

    def scan_around(self):
        self.start_logging()
        self.commander.rotate_right(180, ROTATION_SCAN_VELOCITY)
        self.stop_loging()
        self.commander.rotate_right(180, ROTATION_SCAN_VELOCITY)

    def scan_z_shaped(self, position, width, height):
        """
        :param position: bottom left point of object
        :param width: object width
        :param height: object height
        :return: nothing
        """
        x = position[0]
        y_left, y_right = float(position[1]), float(position[1] + width)
        start_z, end_z = position[2], position[2] + height
        steps_count = int(height / VERTICAL_DELTA)

        self.start_logging()
        for i in range(steps_count):
            self.commander.goto(x, y_right if i % 2 == 0 else y_left, start_z + i * VERTICAL_DELTA, velocity=SCANNING_GOTO_VELOCITY)
        self.stop_loging()

    def _init_logger(self):
        self.logger = Logger(self.scf.cf.log)
        self.logger.add_pos_listener(self.pos_data_cb)
        self.logger.add_measurement_listener(self.meas_data_cb)
        self.logger.add_power_listener(self.power_data_cb)

    def pos_data_cb(self, timestamp, data, logconf):
        self.position = [
            data['stateEstimate.x'],
            data['stateEstimate.y'],
            data['stateEstimate.z']
        ]

    def meas_data_cb(self, timestamp, data, logconf):
        measurement = {
            'roll': data['stabilizer.roll'],
            'pitch': data['stabilizer.pitch'],
            'yaw': data['stabilizer.yaw'],
            'front': data['range.front'],
            'back': data['range.back'],
            'up': data['range.up'],
            'down': data['range.zrange'],
            'left': data['range.left'],
            'right': data['range.right']
        }
        self.on_data_received.call(timestamp, {"measurement": measurement, "pos": self.position}, logconf)

    def power_data_cb(self, timestamp, data, logconf):
        battery = {
            "voltage": data["pm.vbat"],
            "charge": data["pm.chargeCurrent"],
            "batteryLevel": data["pm.batteryLevel"]
        }
        print(battery)
        self.battery_state = battery

    def disconnect(self):
        self.scf.close_link()

    def calibrate(self):
        pass


class DronesFactory:
    def __init__(self, measurement_listener):
        self._measurement_listener = measurement_listener

    def construct(self, uris):
        return [Drone(uri, self._measurement_listener) for uri in uris]

