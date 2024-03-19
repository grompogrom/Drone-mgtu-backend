import random
import time
from cmath import cos, sin, pi

from app.auth.repos import dronesRepo, mapRepo
import matplotlib.pyplot as plt


def visualize(points):
    colors = [0]
    fig = plt.figure()
    # ax = fig.add_subplot(projection='3d')
    ax = fig.add_subplot()

    for point in points:
        ax.scatter(point[0], point[1], c=colors, s=3)
    ax.invert_yaxis()
    plt.show()


if __name__ == '__main__':
    dronesRepo.connect()
    dronesRepo.start_scan()
    dronesRepo.end_of_session()
    points = mapRepo.get_map()

    # points = [[5*cos((i* 2*pi/100).real), 5*sin((i*2*pi/100).real), i] for i in range(100)]
    visualize(points)
