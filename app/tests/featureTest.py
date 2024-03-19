import numpy as np
if __name__ == '__main__':
    pts = np.random.randint(0, 100, (10, 3))
    pts.put((0,2,7),0 )
    print(pts)