"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
from size import Size

class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self._size = Size(1,1)
		
	def get_size(self):
		return self._size
		
	def get_name(self):
		return "Point at " + str(self.x) + ", " + str(self.y)