from cmath import exp, sqrt

from matplotlib import pyplot as plt
from matplotlib.pyplot import contourf


class RadiationMap():
    def __init__(self, radiation_points= [(1800, 180), (120, 1500)]):
        self.length = 2000
        self.width = 2000
        self.map = [[0 for i in range(self.width)] for j in range(self.length)]
        self.focuses = radiation_points

    def fill_map(self):
        for point in self.focuses:
            self.fill_point(point)

    def fill_point(self, point):
        x, y = point
        for i in range(self.length):
            for j in range(self.width):
                self.map[i][j] += 1000 * (-1*sqrt((i - x)**2 + (j - y)**2)**(1/5)).real


if __name__ == '__main__':
    mapp = RadiationMap()
    mapp.fill_map()
    cs = contourf(mapp.map, levels=1000)
    cbar = plt.colorbar(cs)
    plt.show()

