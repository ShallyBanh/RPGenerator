
class Map:
	"""
    Map Class
    args:
        None for now
    """

	def __init__(self, width, height):
        self._size = (width, height)
        self._tileset = None

    def get_size(self):
        return self._size

    def set_size(self, width, height):
        self._size = (width, height)

    def get_tileset(self):
        return _tileset

    def set_tileset(self, tileset):
        self._tileset = tileset