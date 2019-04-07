"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
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
    
    def is_within_range(self, target, x, y):
        return (self.get_x_coordinate() + x <= target.get_x_coordinate() and 
                self.get_x_coordinate() - x >= target.get_x_coordinate() and
                self.get_y_coordinate() + x <= target.get_y_coordinate() and
                self.get_y_coordinate() - x >= target.get_y_coordinate())