class Location:
    """
    Location Class
    """

    def __init__(self):
        self._x = None
        self._y = None
    
    def get_x_coordinate(self):
        return self._x

    def set_x_coordinate(self, x):
        self._x = x
    
    def get_y_coordinate(self):
        return self._y

    def set_y_coordinate(self, y):
        self._y = y