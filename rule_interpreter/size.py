class Size:
    """
    Size Class
    """

    def __init__(self, width, height):
        self._width = width
        self._height = height
    
    def get_width(self):
        return self._width

    def set_width(self, width):
        self._width = width
    
    def get_height(self):
        return self._height

    def set_height(self, height):
        self._height = height