"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
class Size:
    """
    Size Class
    """

    def __init__(self, width, height):
        self.set_width(width)
        self.set_height(height)
    
    def get_width(self):
        return self._width
    
    def get_width_as_string(self):
        return str(self.get_width())

    def set_width(self, width):
        if int(width) < 1:
            raise Exception("Width must be at least 1. Received width was " + str(width) + ".")
        self._width = int(width) 
    
    def get_height(self):
        return self._height
        
    def get_height_as_string(self):
        return str(self.get_height())

    def set_height(self, height):
        if int(height) < 1:
            raise Exception("Height must be at least 1. Received height was " + str(height) + ".")
        self._height = int(height)