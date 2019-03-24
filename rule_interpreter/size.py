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
        if width < 1:
            raise Exception("Width must be at least 1. Received width was " + str(width) + ".")
        self._width = width
    
    def get_height(self):
        return self._height
        
    def get_height_as_string(self):
        return str(self.get_height())

    def set_height(self, height):
        if height < 1:
            raise Exception("Height must be at least 1. Received height was " + str(height) + ".")
        self._height = height