from size import Size

class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self._size = Size(1,1)
		
	def get_size(self):
		return self._size