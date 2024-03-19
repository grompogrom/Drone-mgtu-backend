from cmath import sqrt
from time import sleep

from cflib.crazyflie import HighLevelCommander

from app.jobs.config.flying import TAKE_OFF_VELOCITY, GOTO_VELOCITY


class MotionCommander:
    def __init__(self, cf, default_height=0.4):
        self.default_height = default_height
        self.cf_commander: HighLevelCommander = cf.high_level_commander

    def take_off(self):
        time = self.default_height / TAKE_OFF_VELOCITY
        self.cf_commander.takeoff(self.default_height, time)
        sleep(time)

    def rotate_right(self, angle, velocity):
        time = angle / velocity
        self.cf_commander.go_to(0, 0, 0, -angle, time, relative=True)
        sleep(time)

    def goto(self, x, y, z, velocity=GOTO_VELOCITY):
        distance = sqrt(x*x + y*y + z*z)
        time = (distance / velocity).real
        self.cf_commander.go_to(x, y, z, 0.0, time)
        sleep(time)

    def land(self, landing_height):
        time = 3
        self.cf_commander.land(landing_height, time)
        sleep(time)
