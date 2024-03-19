class PointCloud:
    def __init__(self,save_func):
        self._points_array = []
        self._dots = []
        self._save_func = save_func

    def add(self, elements: list):
        self._dots.extend(elements)
        for element in elements:
            self._points_array.append(element["point"])

    def get_points(self):
        return self._points_array

    def clear_map(self):
        self._points_array.clear()
        self._dots.clear()

    def get_filtered_points(self, sensor: set):
        """
        :param sensor: can be set of front, back, left, right, up, down
        :return:
        """
        filtered = []
        for dot in self._dots:
            if dot["sensor"] in sensor:
                filtered.append(dot["point"])
        return filtered

    def save(self):
        self._save_func(self._dots)