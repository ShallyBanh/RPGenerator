import re
import random
class Attribute:
	# name = ""
	# value = None
		
	def __init__(self, name, value):
		self._name = name.lower()
		self._value = value
		
	def get_attribute_name(self):
		return self._name
		
	def set_attribute_name(self, name):
		self._name = name
		
	def get_attribute_value(self):
		return self._value
		
	def set_attribute_value(self, value):
		self._value = value

class Relationship:
	def __init__(self, ruleContent):
		self._ruleContent = ruleContent
		self._interruptLine = ruleContent.splitlines()[0]
		self._interruptBehaviour = "\n".join(ruleContent.splitlines()[1:])
		
	def get_interrupt_line(self):
		return self._interruptLine
		
	def get_interrupt_behaviour(self):
		return self._interruptBehaviour
		
class Action:
	def __init__(self, name, content):
		self._actionName = name
		self._ruleContent = content
		
	def get_action_name(self):
		return self._actionName
	
	def set_action_name(self, name):
		self._actionName = name
		
	def get_rule_content(self):
		return self._ruleContent
		
	def set_rule_content(self, ruleContent):
		self._ruleContent = ruleContent
		
class Size:
	# width = 1
	# height = 1
	def __init__(self, width, height):
		if height > 0 and width > 0:
			self._width = width
			self._height = height
		else:
			raise Exception("width and height must be greater than 0. The given value of width was " + str(width) + " and the given value of height was " + str(height))
			
	def get_width(self):
		return self._width
		
	def set_width(self, width):
		self._width = width
		
	def get_height(self):
		return self._height
		
	def set_height(self, height):
		self._height = height
	
class Entity:
	
	# x = 0
	# y = 0
	# name = ""
	# type = ""
	# attributes = []
	# size = Size()
	# statuses = []
		
	def __init__(self, name, type, isTemplate):
		self._name = name
		self._type = type
		self._id = None
		self._actions = []
		self._attributes = []
		self._size = Size(1,1)
		self._isTemplate = isTemplate
		self._statuses = []
		self.x = 0
		self.y = 0
		#Validator???
			
	def get_type(self):
		return self._type
		
	def set_type(self, type):
		self._type = type
		
	def get_name(self):
		return self._name
		
	def set_name(self, name):
		self._name = name
		
	def get_id(self):
		return self._id
		
	def set_id(self, id):
		self._id = id
	
	def get_actions(self):
		return self._actions
		
	def set_actions(self, actions):
		self._actions = actions
		
	def add_action(self, action):
		self._actions.append(action)
			
	def add_attribute(self, attribute):
		#print(self.name)
		self._attributes.append(attribute)
		#print(self.attributes)
		
	def get_attribute(self, attributeName):
		attributeName = attributeName.lower()
		for a in self._attributes:
			if a.get_attribute_name() == attributeName:
				return a
		print("No attribute of name " + attributeName + " found.")
				
	def set_attributes(self, attributes):
		self._attributes = attributes
		
	def get_all_attributes(self):
		return self._attributes
		
	def get_size(self):
		return self._size
		
	def set_size(self, size):
		self._size = size
		
	def get_is_template(self):
		return self._isTemplate
		
	def set_is_template(self, isTemplate):
		self._isTemplate = isTemplate
				
	def add_status(self, statusString):
		self._statuses.append(statusString)
		
	def remove_status(self, statusString):
		self._statuses.remove(statusString)
		
	def get_current_statuses(self):
		return self._statuses
		
	def set_current_statuses(self, statuses):
		self._statuses = statuses
		
	def __str__(self):
		attrs = ""
		for a in self._attributes:
			attrs += a.get_attribute_name() + ":" + str(a.get_attribute_value()) + " "
		return "Name: " + self._name + " Type: " + self._type + attrs
		
class Point:
	# x = 0
	# y = 0
	
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self._size = Size(1,1)
		
	def get_size(self):
		return self._size


class RuleEnactor:
	"""
	Rule Enactor class. Takes rules from rule interpreter and assists game engine/view with implementing them.
	"""
	
			
	valid_dice_regex = "^[0-9]*d[0-9]+$"
	
	# all_created_entities = []
	
	##see bottom
	# keywords = {}
	
	##see bottom
	# operators = {}
	
	##key: variable name (string), value: variable value
	# variables = {}
	
	##list of relationships
	# relationships = []
	
	# current_entity_in_loop = None
	
	# target_of_action = None
	
	# acting_entity = None
	
	# current_action = None
	
	# interrupting_relationship = None
	
	
	def __init__(self):
		self.selected_item = None
		self.all_created_entities = []
		#key: variable name (string), value: variable value
		self.variables = {}
		self.relationships = []
		self.current_entity_in_loop = None
		self.target_of_action = None
		self.acting_entity = None
		self.current_action = None
		self.interrupting_relationship = None
		
		
	def add_new_entity(self, entity):
		self.all_created_entities.append(entity)
		
	def get_entity(self, name):
		for e in self.all_created_entities:
			if e.get_name() == name:
				return e
		
	def add_all_entities(self, line):
		return None
		#print("TODO")
		#TODO
	
	def add_all_relationships(self, line):
		return None
		#print("TODO")
		#TODO
		
	def add_new_relationship(self, relationship):
		self.relationships.append(relationship)
				
	def _is_number(self, s):
		try: 
			float(s)
		except ValueError:
			return False
		return True
		
	def perform_action(self, action, acting_entity):
		# ...
		# parse out the target type from the action (Entity or point)
		self.current_action = action
		written_rule = action.get_rule_content()
		lines = written_rule.splitlines()
		#set self here
		self.acting_entity = acting_entity
		# perform each line
		perform_interrupt = False
		for line in lines:
			result = self.evaluate_line(line)
			if result == 'INTERRUPT':
				perform_interrupt = True
				break
		if perform_interrupt:
			# evaluate the relationship
			interrupt_lines = self.interrupting_relationship.get_interrupt_behaviour().splitlines()
			for line in interrupt_lines:
				self.evaluate_line(line)
			
		
	def evaluate_line(self, line):
		line = line.lower()
		words = line.strip().split()
		#base cases:
		# just a number
		if self._is_number(words[0]) and len(words) == 1:
			return float(words[0])
		# a string literal
		if words[0][0] == "\"" and words[0][-1] == "\"":
			return words[0].strip("\"")
		# a boolean literal
		if words[0] == "true":
			return True
		if words[0] == "false":
			return False
		# a dice roll
		elif re.search(self.valid_dice_regex, words[0]) and len(words) == 1:
			return self.roll_dice(words[0])
		# calling a 'function' with a keyword
		elif words[0] in self.keywords:
			return self.keywords[words[0]](self, line)
		#using an operator 
		#serach for boolean operators first (and/or)
		lowest_idx = 999
		first_operator = ''
		for operator in self.boolean_operators:
			check = line.split(operator)
			# do this since we want to solve things left to right
			if len(check) > 1:
				if (lowest_idx > len(check[0])):
					lowest_idx = len(check[0])
					first_operator = operator
		if len(first_operator) > 0:
			return self.boolean_operators[first_operator](self, line)
		#search for combined operators first, since they mess with parsing for just standard operators
		lowest_idx = 999
		first_operator = ''
		for operator in self.combined_operators:
			check = line.split(operator)
			# do this since we want to solve things left to right
			if len(check) > 1:
				if (lowest_idx > len(check[0])):
					lowest_idx = len(check[0])
					first_operator = operator
		if len(first_operator) > 0:
			return self.combined_operators[first_operator](self, line)
		# we also need to consider the case where operators are used without spaces
		lowest_idx = 999
		first_operator = ''
		for operator in self.operators:
			check = line.split(operator)
			# do this since we want to solve things left to right
			if len(check) > 1:
				if (lowest_idx > len(check[0])):
					lowest_idx = len(check[0])
					first_operator = operator
		if len(first_operator) > 0:
			return self.operators[first_operator](self, line)
		# might be an attribute of an entity
		entity_attribute = line.split('.')
		if len(entity_attribute) > 1:
			if entity_attribute[0] == 'self':
				for attr in self.acting_entity.get_all_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
			elif entity_attribute[0] == 'target':
				for attr in self.target_of_action.get_all_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
			elif entity_attribute[0] == self.current_entity_in_loop.get_type():
				for attr in self.current_entity_in_loop.get_all_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
		
		# something else (a variable)
		if not self._is_number(words[0]) and len(words) == 1:
			return self.variables[words[0]]
		
		
	def handle_target(self, line):
		line = line.strip(':')
		words = line.split()
		target_type = words[1]
		# they can either be targeting a point or an entity
		#point case:
		#TODO: we need to be calling a GUI function to give us a point. For now, this is hard coded in. 
		if words[1] == 'point':
			self.target_of_action = Point(1,1)
		# entity case:
		#TODO: in reality we need to be calling a GUI function that gives us the targeted entity...
		#thus this is a placeholder for now
		else:
			for entity in self.all_created_entities:
				if entity.get_name() == target_type:
					self.target_of_action = entity
					#print("New Target :")
					#print(self.target_of_action)
		#TODO: We need to potentially interrupt the recursive flow here by returning an INTERRUPT code, in case there is a relationship that overrides this behaviour
		for r in self.relationships:
			if self.check_for_interrupt(r) == 'INTERRUPT':
				return 'INTERRUPT'
		
	
	def check_for_interrupt(self, relationship):
		interrupt_line = relationship.get_interrupt_line().strip(':')
		words = interrupt_line.split()
		entity_action = words[1].split('.')
		if self.acting_entity.get_type() == entity_action[0] and self.current_action.get_action_name() == entity_action[1]:
			conditional = interrupt_line.split(' if ')
			if self.evaluate_line(conditional[1]) == True:
				self.interrupting_relationship = relationship
				return 'INTERRUPT'
	
	
	def handle_if(self, line):
		# handle all case
		original_line = line
		if 'all' in line:
			line = line.replace('all', '')
			post_if = line.split('if')[1].strip()
			#print(post_if)
			conditional_and_action = post_if.split('then')
			#print(conditional_and_action)
			conditional = conditional_and_action[0].strip()
			action = conditional_and_action[1].strip()
			
			for entity in self.all_created_entities:
				#print("all created entities: " + str(self.all_created_entities))
				#print("Setting current entitiy in loop to" + str(entity))
				self.current_entity_in_loop = entity
				tf = self.evaluate_line(conditional)
				#print("Did said entity satisfy condition?")
				#print(tf)
				if tf:
					self.evaluate_line(action)
				self.current_entity_in_loop = None
		else:
			post_if = line.split('if')[1].strip()
			#print(post_if)
			conditional_and_action = post_if.split('then')
			#print(conditional_and_action)
			conditional = conditional_and_action[0].strip()
			action = conditional_and_action[1].strip()
			
			if self.evaluate_line(conditional):
				return self.evaluate_line(action)
	
	def handle_increase(self, written_rule):
		#handle increasing something. Expecting: increase x by y (by is optional)
		if "by" in written_rule:
			remove_idx = 3
		else:
			remove_idx = 2
		words = written_rule.split()
		# we are either increasing a variable or an attribute of an entity
		# variable case:
		rest_of_sentence = words[remove_idx:]
		if words[1] in self.variables:
			self.variables[words[1]] += self.evaluate_line(" ".join(rest_of_sentence))
		# must be increasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(" ".join(rest_of_sentence)))
		
	def handle_decrease(self, written_rule):
		#handle decreasing something. Expecting: decrease x by y (by is optional)
		if "by" in written_rule:
			remove_idx = 3
		else:
			remove_idx = 2
		words = written_rule.split()
		# we are either increasing a variable or an attribute of an entity
		# variable case:
		rest_of_sentence = words[remove_idx:]
		if words[1] in self.variables:
			self.variables[words[1]] -= self.evaluate_line(" ".join(rest_of_sentence))
		# must be decreasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(" ".join(rest_of_sentence)))
		
	def handle_multiply(self, written_rule):
		#handle multiplying something. Expecting: multiply x by y (by is optional)
		if "by" in written_rule:
			remove_idx = 3
		else:
			remove_idx = 2
		words = written_rule.split()
		# we are either increasing a variable or an attribute of an entity
		# variable case:
		rest_of_sentence = words[remove_idx:]
		if words[1] in self.variables:
			self.variables[words[1]] *= self.evaluate_line(" ".join(rest_of_sentence))
		# must be multiplying entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(" ".join(rest_of_sentence)))
		
	def handle_divide(self, written_rule):
		#handle dividing something. Expecting: divide x by y (by is optional)
		if "by" in written_rule:
			remove_idx = 3
		else:
			remove_idx = 2
		words = written_rule.split()
		# we are either increasing a variable or an attribute of an entity
		# variable case:
		rest_of_sentence = words[remove_idx:]
		if words[1] in self.variables:
			self.variables[words[1]] /= self.evaluate_line(" ".join(rest_of_sentence))
		# must be dividing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(" ".join(rest_of_sentence)))
		
	def handle_set(self, written_rule):
		#handle setting something. Expecting: set x to y (to is optional)
		if "to" in written_rule:
			remove_idx = 3
		else:
			remove_idx = 2
		words = written_rule.split()
		# we are either increasing a variable or an attribute of an entity
		# variable case:
		rest_of_sentence = words[remove_idx:]
		if len(words[1].split('.')) < 2:
			self.variables[words[1]] = self.evaluate_line(" ".join(rest_of_sentence))
		# must be setting entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(" ".join(rest_of_sentence)))
		
	def handle_within(self, written_rule):
		#TODO: Not currently considering the size in this calculation
		# expecting: item1 within(3,3) of item2
		# or:		 item1 within (3, 3) of item2
		# handle detecting entities within a given distance of the selection
		# item1/2 may be: a point, a target entity, the acting_entity, or referring to a general type of
		# entities. We must determine the case.
		# We know at least one of item1/2 is referring to a specific target (point, entity, or self), and only one could possibly be a general type.
		item1 = None
		item2 = None
		words = written_rule.split()
		item1_string = words[0]
		item2_string = words[-1]
		if item1_string == 'self':
			item1 = self.acting_entity
		elif item1_string == 'target':
			item1 = self.target_of_action
		elif item1_string == self.current_entity_in_loop.get_type():
			item1 = self.current_entity_in_loop
			##print("setting current entity in loop to" + str(self.current_entity_in_loop))
		#item 2
		if item2_string == 'self':
			item2 = self.acting_entity
		elif item2_string == 'target':
			item2 = self.target_of_action
		elif item2_string == self.current_entity_in_loop.get_type():
			item2 = self.current_entity_in_loop
			##print("setting current entity in loop to" + statuses(self.current_entity_in_loop))
		
		left_bracket_idx = written_rule.find('(')
		right_bracket_idx = written_rule.find(')')
		given_args = written_rule[left_bracket_idx+1:right_bracket_idx]
		ints = [x.strip() for x in given_args.split(',')]
		x_dist = int(ints[0])
		y_dist = int(ints[1])
		
		within_x = False
		within_y = False
		if item1 is not None and item2 is not None:
			# x cases
			if item1.x < item2.x:
				if item1.x + item1.get_size().get_width() - 1 + x_dist >= item2.x:
					within_x = True
			elif item1.x > item2.x:
				if item1.x - x_dist <= item2.x + item2.get_size().get_width() - 1:
					within_x = True
			elif item1.x == item2.x:
				within_x = True
			# y cases	
			if item1.y < item2.y:
				if item1.y + y_dist + item1.get_size().get_height() - 1 >= item2.y:
					within_y = True
			elif item1.y > item2.y:
				if item1.y - y_dist <= item2.y + item2.get_size().get_width() - 1:
					within_y = True
			elif item1.y == item2.y:
				within_y = True
			# therefore, is within? 
			if within_y and within_x:
				return True
			return False
				
		
	def handle_move(self, written_rule):
		if "towards" in written_rule:
			self.handle_movetowards(written_rule)
		elif "away" in written_rule:
			self.handle_moveaway(written_rule)
		
	def handle_moveaway(self, written_rule):
		# handle moving targets away from a given point or entity
		words = written_rule.split()
		entity_to_move = None
		item_to_move_from = None
		entity_to_move_string = words[1]
		item_to_move_string = words[-1]
		distance_to_move = int(words[2])
		if entity_to_move_string == 'self':
			entity_to_move = self.acting_entity
		elif entity_to_move_string == 'target':
			entity_to_move = self.target_of_action
		elif entity_to_move_string == current_entity_in_loop.get_type():
			entity_to_move = self.current_entity_in_loop
		
		if item_to_move_string == 'self':
			item_to_move_from = self.acting_entity
		elif item_to_move_string == 'target':
			item_to_move_from = self.target_of_action
		elif item_to_move_string == self.current_entity_in_loop.get_type():
			item_to_move_from = self.current_entity_in_loop
			
		if entity_to_move == item_to_move_from:
			return
			
		x_dist = entity_to_move.x - item_to_move_from.x
		y_dist = entity_to_move.y - item_to_move_from.y
		# move horizontally 
		if abs(x_dist) >= abs(y_dist):
			if x_dist < 0:
				#entity to move is to the left, so move more left
				
				entity_to_move.x -= distance_to_move
			else:
				# otherwise go right
				entity_to_move.x += distance_to_move
		else:
			#move vertically
			if y_dist < 0:
				entity_to_move.y -= distance_to_move
			else:
				# otherwise go right
				entity_to_move.y += distance_to_move
		
	def handle_movetowards(self, written_rule):
		# handle moving targets away from a given point or entity
		words = written_rule.split()
		entity_to_move = None
		item_to_move_from = None
		entity_to_move_string = words[1]
		item_to_move_string = words[-1]
		distance_to_move = int(words[2])
		if entity_to_move_string == 'self':
			entity_to_move = self.acting_entity
		elif entity_to_move_string == 'target':
			entity_to_move = self.target_of_action
		elif entity_to_move_string == current_entity_in_loop.get_type():
			entity_to_move = self.current_entity_in_loop
		
		if item_to_move_string == 'self':
			item_to_move_from = self.acting_entity
		elif item_to_move_string == 'target':
			item_to_move_from = self.target_of_action
		elif item_to_move_string == self.current_entity_in_loop.get_type():
			item_to_move_from = self.current_entity_in_loop
			
		if entity_to_move == item_to_move_from:
			return
			
		x_dist = entity_to_move.x - item_to_move_from.x
		y_dist = entity_to_move.y - item_to_move_from.y
		# move horizontally 
		if abs(x_dist) >= abs(y_dist):
			if abs(x_dist) < distance_to_move:
					distance_to_move = abs(x_dist)
			if x_dist < 0:
				#entity to move is to the left, so move more left
				entity_to_move.x += distance_to_move
			else:
				# otherwise go right
				entity_to_move.x -= distance_to_move
		else:
			#move vertically
			if abs(y_dist) < distance_to_move:
					distance_to_move = abs(y_dist)
			if y_dist < 0:
				entity_to_move.y += distance_to_move
			else:
				# otherwise go right
				entity_to_move.y -= distance_to_move
		
	def handle_plus(self, written_rule):
		words = written_rule.split('+')
		return self.evaluate_line(words[0].strip()) + self.evaluate_line(words[1].strip())
		
	def handle_minus(self, written_rule):
		words = written_rule.split('-')
		return self.evaluate_line(words[0].strip()) - self.evaluate_line(words[1].strip())
		
	def handle_equals(self, written_rule):
		words = written_rule.split('==')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) == self.evaluate_line(words[1].strip())
		words = written_rule.split('equals')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) == self.evaluate_line(words[1].strip())
		
	def handle_less_than(self, written_rule):
		words = written_rule.split('<')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) < self.evaluate_line(words[1].strip())
		words = written_rule.split('less than')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) < self.evaluate_line(words[1].strip())
		
	def handle_greater_than(self, written_rule):
		words = written_rule.split('>')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) > self.evaluate_line(words[1].strip())
		words = written_rule.split('greater than')
		if len(words) > 1:
			return self.evaluate_line(words[0].strip()) > self.evaluate_line(words[1].strip())
		
	def handle_multiply_operator(self, written_rule):
		words = written_rule.split('*')
		return self.evaluate_line(words[0].strip()) * self.evaluate_line(words[1].strip())
		
	def handle_divide_operator(self, written_rule):
		words = written_rule.split('/')
		return self.evaluate_line(words[0].strip()) / self.evaluate_line(words[1].strip())
		
	def handle_assignment(self, written_rule):
		words = written_rule.split('=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(words[1].strip()))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self.evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] = self.evaluate_line(words[1].strip())
		
	def handle_plus_equals(self, written_rule):
		words = written_rule.split('+=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(words[1].strip()))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self.evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] += self.evaluate_line(words[1].strip())
		
	def handle_minus_equals(self, written_rule):
		words = written_rule.split('-=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(words[1].strip()))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self.evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] -= self.evaluate_line(words[1].strip())
	
	def handle_times_equals(self, written_rule):
		words = written_rule.split('*=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(words[1].strip()))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self.evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] *= self.evaluate_line(words[1].strip())
			
	def handle_divide_equals(self, written_rule):
		words = written_rule.split('/=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(words[1].strip()))
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				for attribute in self.current_entity_in_loop.get_all_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self.evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] /= self.evaluate_line(words[1].strip())
	
	def handle_and(self, written_rule):
		words = written_rule.split('and')
		return self.evaluate_line(words[0].strip()) and self.evaluate_line(words[1].strip())
		
	def handle_or(self, written_rule):
		words = written_rule.split('or')
		return self.evaluate_line(words[0].strip()) or self.evaluate_line(words[1].strip())
		
	def handle_add_status(self, written_rule):
		words = written_rule.split()
		status_to_add = words[2].strip('"')
		affected_entity_string = words[-1]
		if affected_entity_string == 'self':
			self.acting_entity.add_status(status_to_add)
		elif affected_entity_string == 'target':
			self.target_of_action.add_status(status_to_add)
		elif affected_entity_string == self.current_entity_in_loop.get_type():
			self.current_entity_in_loop.add_status(status_to_add)
			
	def handle_remove_status(self, written_rule):
		words = written_rule.split()
		status_to_remove = words[2].strip('"')
		affected_entity_string = words[-1]
		if affected_entity_string == 'self':
			self.acting_entity.remove_status(status_to_remove)
		elif affected_entity_string == 'target':
			self.target_of_action.remove_status(status_to_remove)
		elif affected_entity_string == self.current_entity_in_loop.get_type():
			self.current_entity_in_loop.remove_status(status_to_remove)
		
	def handle_has_status(self, written_rule):
		words = written_rule.split('has')
		status_to_check = words[1].strip().strip('"')
		entity_info = words[0].strip().split('.')
		if entity_info[1] == 'statuses':
			if entity_info[0] == 'self':
				return status_to_check in self.acting_entity.get_current_statuses()
			elif entity_info[0] == 'target':
				return status_to_check in self.target_of_action.get_current_statuses()
			elif entity_info[0] == self.current_entity_in_loop.get_type():
				return status_to_check in self.current_entity_in_loop.get_current_statuses()
	
	def roll_dice(self, dice_string):
		roll_data = dice_string.split('d')
		if roll_data[1] == '1' or roll_data[1] == '0':
			return int(roll_data[1])
		else:
			if roll_data[0] == '':
				return random.randint(1,int(roll_data[1]))
			else:
				total = 0
				for i in range(int(roll_data[0])):
					total += random.randint(1,int(roll_data[1]))
				return total
	
	
		
		
	keywords = {"target":handle_target, "if":handle_if, 
				"increase":handle_increase,"decrease":handle_decrease, "multiply":handle_multiply,
				"divide":handle_divide, "set":handle_set, "reduce":handle_decrease, 
				"move":handle_move, "add":handle_add_status, "remove":handle_remove_status}
				
	combined_operators = {"+=":handle_plus_equals, "-=":handle_minus_equals, 
				"*=":handle_times_equals, "/=":handle_divide_equals, "==":handle_equals,}
				
	operators = {" within(":handle_within, "+": handle_plus, "-":handle_minus,  
				" equals ":handle_equals, "<":handle_less_than, ">":handle_greater_than, 
				" less ":handle_less_than, " greater ": handle_greater_than, "*": handle_multiply_operator,
				"/":handle_divide_operator, "=":handle_assignment, " has ":handle_has_status}
				
	boolean_operators = {" and ":handle_and, " or ":handle_or}