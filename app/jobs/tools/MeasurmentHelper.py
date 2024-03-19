import math

import numpy as np

from app.jobs.config.scaning import SENSOR_TH, PLOT_SENSOR_DOWN


def _rot(roll, pitch, yaw, origin, point):
    cosr = math.cos(math.radians(roll))
    cosp = math.cos(math.radians(pitch))
    cosy = math.cos(math.radians(yaw))

    sinr = math.sin(math.radians(roll))
    sinp = math.sin(math.radians(pitch))
    siny = math.sin(math.radians(yaw))

    roty = np.array([[cosy, -siny, 0],
                     [siny, cosy, 0],
                     [0, 0, 1]])

    rotp = np.array([[cosp, 0, sinp],
                     [0, 1, 0],
                     [-sinp, 0, cosp]])

    rotr = np.array([[1, 0, 0],
                     [0, cosr, -sinr],
                     [0, sinr, cosr]])

    rotFirst = np.dot(rotr, rotp)

    rot = np.array(np.dot(rotFirst, roty))

    tmp = np.subtract(point, origin)
    tmp2 = np.dot(rot, tmp)
    res: list[float] = list(np.add(tmp2, origin))
    return res


def measurments_to_points(meas, drone_pos, timestamp):
    data = []
    roll = meas['roll']
    pitch = -meas['pitch']
    yaw = meas['yaw']

    if meas['up'] < SENSOR_TH:
        up = [drone_pos[0], drone_pos[1], drone_pos[2] + meas['up'] / 1000.0]
        data.append(
            {
                "sensor": "up",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, up)
            }
        )

    if meas['down'] < SENSOR_TH and PLOT_SENSOR_DOWN:
        down = [drone_pos[0], drone_pos[1], drone_pos[2] - meas['down'] / 1000.0]
        data.append(
            {
                "sensor": "down",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, down)
            }
        )

    if meas['left'] < SENSOR_TH:
        left = [drone_pos[0], drone_pos[1] + meas['left'] / 1000.0, drone_pos[2]]
        data.append(
            {
                "sensor": "left",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, left)
            }
        )

    if meas['right'] < SENSOR_TH:
        right = [drone_pos[0], drone_pos[1] - meas['right'] / 1000.0, drone_pos[2]]
        data.append(
            {
                "sensor": "right",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, right)
            }
        )

    if meas['front'] < SENSOR_TH:
        front = [drone_pos[0] + meas['front'] / 1000.0, drone_pos[1], drone_pos[2]]
        data.append(
            {
                "sensor": "front",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, front)
            }
        )

    if meas['back'] < SENSOR_TH:
        back = [drone_pos[0] - meas['back'] / 1000.0, drone_pos[1], drone_pos[2]]
        data.append(
            {
                "sensor": "back",
                "timestamp": timestamp,
                "point": _rot(roll, pitch, yaw, drone_pos, back)
            }
        )

    return data
