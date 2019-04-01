import re
import random
import sys
import copy
sys.path.append('../rule_interpreter/models')
from entity import Entity
from action import Action
from attribute import Attribute
from relationship import Relationship
from size import Size
from point import Point	
from validator import _Validator

class RuleEnactor:
	"""
	Rule Enactor class. Takes rules from rule interpreter and assists game engine/view with implementing them.
	"""
	
			
	valid_dice_regex = "^[0-9]*d[0-9]+$"
	
	def __init__(self):
		self.selected_item = None
		self.entity_types = []
		self.concrete_entity_types = []
		# key: (x,y), value: entity
		self.all_created_entities = {}
		
		#key: variable name (string), value: variable value
		self.variables = {}
		self.relationships = []
		self.current_entity_in_loop = None
		self.target_of_action = None
		self.acting_entity = None
		self.current_action = None
		self.interrupting_relationship = None
		
	def add_new_entity(self, entityType, name = "", x = 0, y = 0):
		#self.all_created_entities.append(entity)
		if (x,y) in self.all_created_entities.keys():
			raise Exception("An entity already exists at this location")
			return None
		newEntity = None
		for e in self.concrete_entity_types:
			if e.is_of_type(entityType):
				newEntity = copy.deepcopy(e)
				break
		if newEntity is None:
			return None
		newEntity.x = x
		newEntity.y = y
		newEntity.set_name(name)
		self.all_created_entities[(newEntity.x,newEntity.y)] = newEntity
		return newEntity
		
	def move_entity(self, entity, new_xy_tuple):
		del self.all_created_entities[(entity.x, entity.y)]
		entity.x = new_xy_tuple[0]
		entity.y = new_xy_tuple[1]
		self.all_created_entities[new_xy_tuple] = entity
		return entity
		
	def remove_entity(self, entity):
		x = entity.x
		y = entity.y
		del self.all_created_entities[(x,y)]
		
	def modify_attribute(self, entity, attributeName, attributeValue):
		entity.get_attribute(attributeName).set_attribute_value(attributeValue)
		
	def get_entity(self, name):
		for key in self.all_created_entities:
			if self.all_created_entities[key].get_name() == name:
				return self.all_created_entities[key]
		
	def parse_validator(self, validator):
		self.relationships = validator.get_relationships()
		self.entity_types = validator.get_entities()
		for e in self.entity_types:
			if not e.get_is_template():
				self.concrete_entity_types.append(e)
				
		
	def add_new_relationship(self, relationship):
		self.relationships.append(relationship)
				
	def _is_number(self, s):
		try: 
			float(s)
		except ValueError:
			return False
		return True
				
	def perform_action(self, action, acting_entity):
		target = self._determine_target(action.get_target_line())
		if target is None:
			return self.perform_action_given_target(action, acting_entity, acting_entity)
		else:
			return target
	
	def perform_action_given_target(self, action, acting_entity, target_entity):
		self.acting_entity = acting_entity
		self.target_of_action = target_entity
		self.current_action = action
		written_rule = action.get_action_behaviour()
		lines = written_rule.splitlines()
		# check for interrupts
		for r in self.relationships:
			if self._check_for_interrupt(r) == 'INTERRUPT':
				interrupt_lines = self.interrupting_relationship.get_interrupt_behaviour().splitlines()
				for line in interrupt_lines:
					self._evaluate_line(line)
				return "The action \"" + action.get_action_name() + "\" was interrupted by the relationship \"" + self.interrupting_relationship.get_name() + "\" while being performed on \"" + target_entity.get_name() + "\" by \"" + acting_entity.get_name() + "\"."
		# otherwise perform the action
		for line in lines:
			result = self._evaluate_line(line)
			
		return "The action \"" + action.get_action_name() + "\" was performed on \"" + target_entity.get_name() + "\" by \"" + acting_entity.get_name() + "\"."
				
			
	def _determine_target(self, target_line):
		words = target_line.strip().strip(':').split()
		if words[1] == 'self':
			# we don't need a new target
			return None
		elif words[1] == 'point':
			# we need to target a point
			return 'point'
		else:
			# we need to target an entity of this type
			return words[1]
		
		
	def _evaluate_line(self, line):
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
				for attr in self.acting_entity.get_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
			elif entity_attribute[0] == 'target':
				for attr in self.target_of_action.get_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
			elif self.current_entity_in_loop.is_of_type(entity_attribute[0]):
				for attr in self.current_entity_in_loop.get_attributes():
					if attr.get_attribute_name() == entity_attribute[1]:
						return attr.get_attribute_value()
		
		# something else (a variable)
		if not self._is_number(words[0]) and len(words) == 1:
			return self.variables[words[0]]
		
		
	def _check_for_interrupt(self, relationship):
		interrupt_line = relationship.get_interrupt_line().lower().strip(':')
		words = interrupt_line.split()
		entity_action = words[1].split('.')
		if self.acting_entity.is_of_type(entity_action[0]) and self.current_action.get_action_name() == entity_action[1]:
			conditional = interrupt_line.split(' if ')
			if self._evaluate_line(conditional[1]) == True:
				self.interrupting_relationship = relationship
				return 'INTERRUPT'
	
	
	def _handle_if(self, line):
		# handle all case
		original_line = line
		if 'all' in line:
			line = line.replace('all', '')
			post_if = line.split('if')[1].strip()
			conditional_and_action = post_if.split('then')
			conditional = conditional_and_action[0].strip()
			action = conditional_and_action[1].strip()
			
			for key in self.all_created_entities:
				self.current_entity_in_loop = self.all_created_entities[key]
				tf = self._evaluate_line(conditional)
				if tf:
					self._evaluate_line(action)
				self.current_entity_in_loop = None
		else:
			post_if = line.split('if')[1].strip()
			conditional_and_action = post_if.split('then')
			conditional = conditional_and_action[0].strip()
			action = conditional_and_action[1].strip()
			
			if self._evaluate_line(conditional):
				return self._evaluate_line(action)
	
	def _handle_increase(self, written_rule):
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
			self.variables[words[1]] += self._evaluate_line(" ".join(rest_of_sentence))
		# must be increasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(" ".join(rest_of_sentence)))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(" ".join(rest_of_sentence)))
		
	def _handle_decrease(self, written_rule):
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
			self.variables[words[1]] -= self._evaluate_line(" ".join(rest_of_sentence))
		# must be decreasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(" ".join(rest_of_sentence)))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(" ".join(rest_of_sentence)))
		
	def _handle_multiply(self, written_rule):
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
			self.variables[words[1]] *= self._evaluate_line(" ".join(rest_of_sentence))
		# must be multiplying entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(" ".join(rest_of_sentence)))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(" ".join(rest_of_sentence)))
		
	def _handle_divide(self, written_rule):
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
			self.variables[words[1]] /= self._evaluate_line(" ".join(rest_of_sentence))
		# must be dividing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(" ".join(rest_of_sentence)))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(" ".join(rest_of_sentence)))
		
	def _handle_set(self, written_rule):
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
			self.variables[words[1]] = self._evaluate_line(" ".join(rest_of_sentence))
		# must be setting entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(" ".join(rest_of_sentence)))
			#targeting target entity
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(" ".join(rest_of_sentence)))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(" ".join(rest_of_sentence)))
		
	def _handle_within(self, written_rule):
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
		elif self.current_entity_in_loop.is_of_type(item1_string.lower()):
			item1 = self.current_entity_in_loop
		#item 2
		if item2_string == 'self':
			item2 = self.acting_entity
		elif item2_string == 'target':
			item2 = self.target_of_action
		elif self.current_entity_in_loop.is_of_type(item2_string.lower()):
			item2 = self.current_entity_in_loop
		
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
				
		
	def _handle_move(self, written_rule):
		if "towards" in written_rule:
			self._handle_movetowards(written_rule)
		elif "away" in written_rule:
			self._handle_moveaway(written_rule)
		
	def _handle_moveaway(self, written_rule):
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
		elif current_entity_in_loop.is_of_type(entity_to_move_string):
			entity_to_move = self.current_entity_in_loop
		
		if item_to_move_string == 'self':
			item_to_move_from = self.acting_entity
		elif item_to_move_string == 'target':
			item_to_move_from = self.target_of_action
		elif self.current_entity_in_loop.is_of_type(item_to_move_string):
			item_to_move_from = self.current_entity_in_loop
			
		if entity_to_move == item_to_move_from:
			return
		
		entity_x = entity_to_move.x
		entity_y = entity_to_move.y
		
		x_dist = entity_to_move.x - item_to_move_from.x
		y_dist = entity_to_move.y - item_to_move_from.y
		# move horizontally 
		if abs(x_dist) >= abs(y_dist):
			if x_dist < 0:
				#entity to move is to the left, so move more left
				entity_x -= distance_to_move
			else:
				# otherwise go right
				entity_x += distance_to_move
		else:
			#move vertically
			if y_dist < 0:
				entity_y -= distance_to_move
			else:
				# otherwise go right
				entity_y += distance_to_move
		self.move_entity(entity_to_move, (entity_x, entity_y))
		
	def _handle_movetowards(self, written_rule):
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
		elif current_entity_in_loop.is_of_type(entity_to_move_string):
			entity_to_move = self.current_entity_in_loop
		
		if item_to_move_string == 'self':
			item_to_move_from = self.acting_entity
		elif item_to_move_string == 'target':
			item_to_move_from = self.target_of_action
		elif self.current_entity_in_loop.is_of_type(item_to_move_string):
			item_to_move_from = self.current_entity_in_loop
			
		if entity_to_move == item_to_move_from:
			return
			
		entity_x = entity_to_move.x
		entity_y = entity_to_move.y
			
		x_dist = entity_to_move.x - item_to_move_from.x
		y_dist = entity_to_move.y - item_to_move_from.y
		# move horizontally 
		if abs(x_dist) >= abs(y_dist):
			if abs(x_dist) < distance_to_move:
					distance_to_move = abs(x_dist) - 1
			if x_dist < 0:
				#entity to move is to the left, so move more left
				entity_x += distance_to_move
			else:
				# otherwise go right
				entity_x -= distance_to_move
		else:
			#move vertically
			if abs(y_dist) < distance_to_move:
					distance_to_move = abs(y_dist) - 1
			if y_dist < 0:
				entity_y += distance_to_move
			else:
				# otherwise go right
				entity_y -= distance_to_move
		self.move_entity(entity_to_move, (entity_x, entity_y))
		
	def _handle_plus(self, written_rule):
		words = written_rule.split('+')
		return self._evaluate_line(words[0].strip()) + self._evaluate_line(words[1].strip())
		
	def _handle_minus(self, written_rule):
		words = written_rule.split('-')
		return self._evaluate_line(words[0].strip()) - self._evaluate_line(words[1].strip())
		
	def _handle_equals(self, written_rule):
		words = written_rule.split('==')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) == self._evaluate_line(words[1].strip())
		words = written_rule.split('equals')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) == self._evaluate_line(words[1].strip())
		
	def _handle_less_than(self, written_rule):
		words = written_rule.split('<')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) < self._evaluate_line(words[1].strip())
		words = written_rule.split('less than')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) < self._evaluate_line(words[1].strip())
		
	def _handle_greater_than(self, written_rule):
		words = written_rule.split('>')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) > self._evaluate_line(words[1].strip())
		words = written_rule.split('greater than')
		if len(words) > 1:
			return self._evaluate_line(words[0].strip()) > self._evaluate_line(words[1].strip())
		
	def _handle_multiply_operator(self, written_rule):
		words = written_rule.split('*')
		return self._evaluate_line(words[0].strip()) * self._evaluate_line(words[1].strip())
		
	def _handle_divide_operator(self, written_rule):
		words = written_rule.split('/')
		return self._evaluate_line(words[0].strip()) / self._evaluate_line(words[1].strip())
		
	def _handle_assignment(self, written_rule):
		words = written_rule.split('=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(words[1].strip()))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(self._evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] = self._evaluate_line(words[1].strip())
		
	def _handle_plus_equals(self, written_rule):
		words = written_rule.split('+=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(words[1].strip()))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() + self._evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] += self._evaluate_line(words[1].strip())
		
	def _handle_minus_equals(self, written_rule):
		words = written_rule.split('-=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(words[1].strip()))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() - self._evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] -= self._evaluate_line(words[1].strip())
	
	def _handle_times_equals(self, written_rule):
		words = written_rule.split('*=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(words[1].strip()))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() * self._evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] *= self._evaluate_line(words[1].strip())
			
	def _handle_divide_equals(self, written_rule):
		words = written_rule.split('/=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(" ".join(rest_of_sentence)))
			elif entity_info[0] == 'target':
				for attribute in self.target_of_action.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(words[1].strip()))
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				for attribute in self.current_entity_in_loop.get_attributes():
					if attribute.get_attribute_name() == entity_info[1]:
						attribute.set_attribute_value(attribute.get_attribute_value() / self._evaluate_line(words[1].strip()))
		else:
			self.variables[words[0].strip()] /= self._evaluate_line(words[1].strip())
	
	def _handle_and(self, written_rule):
		words = written_rule.split('and')
		return self._evaluate_line(words[0].strip()) and self._evaluate_line(words[1].strip())
		
	def _handle_or(self, written_rule):
		words = written_rule.split('or')
		return self._evaluate_line(words[0].strip()) or self._evaluate_line(words[1].strip())
		
	def _handle_add_status(self, written_rule):
		words = written_rule.split()
		status_to_add = self._evaluate_line(words[2])
		affected_entity_string = words[-1]
		if affected_entity_string == 'self':
			self.acting_entity.add_status(status_to_add)
		elif affected_entity_string == 'target':
			self.target_of_action.add_status(status_to_add)
		elif self.current_entity_in_loop.is_of_type(affected_entity_string):
			self.current_entity_in_loop.add_status(status_to_add)
			
	def _handle_remove_status(self, written_rule):
		words = written_rule.split()
		status_to_remove = self._evaluate_line(words[2])
		affected_entity_string = words[-1]
		try:
			if affected_entity_string == 'self':
				self.acting_entity.remove_status(status_to_remove)
			elif affected_entity_string == 'target':
				self.target_of_action.remove_status(status_to_remove)
			elif self.current_entity_in_loop.is_of_type(affected_entity_string):
				self.current_entity_in_loop.remove_status(status_to_remove)
		except:
			pass
		
	def _handle_has_status(self, written_rule):
		words = written_rule.split('has')
		status_to_check = self._evaluate_line(words[1].strip())
		entity_info = words[0].strip().split('.')
		if entity_info[1] == 'statuses':
			if entity_info[0] == 'self':
				return status_to_check in self.acting_entity.get_current_statuses()
			elif entity_info[0] == 'target':
				return status_to_check in self.target_of_action.get_current_statuses()
			elif self.current_entity_in_loop.is_of_type(entity_info[0]):
				return status_to_check in self.current_entity_in_loop.get_current_statuses()
	
	def roll_dice(self, dice_string):
		roll_data = dice_string.split('d')
		if roll_data[1] == '0':
			return int(roll_data[1])
		else:
			if roll_data[0] == '':
				return random.randint(1,int(roll_data[1]))
			try:
				int(roll_data[0])
				int(roll_data[1])
			except:
				return None
			if roll_data[0] == '0':
				return 0
			else:
				if int(roll_data[0]) > 100 or int(roll_data[1]) > 120:
					# apparently, the most number of sides on one dice is 120!
					return None
				total = 0
				for i in range(int(roll_data[0])):
					total += random.randint(1,int(roll_data[1]))
				return total
	
	
		
		
	keywords = {"if":_handle_if, 
				"increase":_handle_increase,"decrease":_handle_decrease, "multiply":_handle_multiply,
				"divide":_handle_divide, "set":_handle_set, "reduce":_handle_decrease, 
				"move":_handle_move, "add":_handle_add_status, "remove":_handle_remove_status}
				
	combined_operators = {"+=":_handle_plus_equals, "-=":_handle_minus_equals, 
				"*=":_handle_times_equals, "/=":_handle_divide_equals, "==":_handle_equals,}
				
	operators = {" within(":_handle_within, "+": _handle_plus, "-":_handle_minus,  
				" equals ":_handle_equals, "<":_handle_less_than, ">":_handle_greater_than, 
				" less ":_handle_less_than, " greater ": _handle_greater_than, "*": _handle_multiply_operator,
				"/":_handle_divide_operator, "=":_handle_assignment, " has ":_handle_has_status}
				
	boolean_operators = {" and ":_handle_and, " or ":_handle_or}