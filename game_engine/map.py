
class Map:
    """
    Map Class
    args:
        tilesize, width, height
    """

    def __init__(self, tilesize, width, height):
        self.width = width
        self.height = height
        self.tilesize = tilesize
        self._tileset = [[0 for w in range(width)] for h in range(height)]

    # def get_width(self):
    #     return self._width

    # def set_width(self, width):
    #     self._width = width

    # def get_height(self):
    #     return self._height

    # def set_height(self, height):
    #     self._height = height

    # def get_tilesize(self):
    #     return self._tilesize

    # def set_tilesize(self, tilesize):
    #     self._tilesize = tilesize

    def get_tileset(self):
        return self._tileset

    def set_tileset(self, tileset):
        self._tileset = tileset
