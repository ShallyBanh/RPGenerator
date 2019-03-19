class Size:
    """
    Size Class
    """

    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def get_width(self):
        return self._width
    
    def get_width_as_string(self):
        return str(self.get_width())

    def set_width(self, width):
        self._width = width
    
    def get_height(self):
        return self._height
        
    def get_height_as_string(self):
        return str(self.get_height())

    def set_height(self, height):
        self._height = height