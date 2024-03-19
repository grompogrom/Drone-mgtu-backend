def save_points_to_file(points):

    with open("PointCloudRes.txt", 'w') as f:
        f.write(str(points))
