
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
        self.textures = []
        self.fogOfWar =  [[True for w in range(width)] for h in range(height)]

    class Texture:
        """
        Inner Texture Class
        args:
            x, y, width, height, name
        """
        def __init__(self, x, y, width, height, name):
            self.width = width
            self.height = height
            self.x = x
            self.y = y
            self.name = name
