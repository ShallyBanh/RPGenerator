import re
import random
class Attribute:
	name = ""
	value = None
		
	def __init__(self, name, value):
		self.name = name
		self.value = value
		
class Size:
	width = 1
	height = 1
	
class Entity:
	
	x = 0
	y = 0
	name = ""
	type = ""
	attributes = []
	size = Size()
	statuses = []
		
	def __init__(self, name, type):
		self.name = name
		self.type = type
			
	def add_attribute(self, attribute):
		self.attributes.append(attribute)


class RuleEnactor:
	"""
	Rule Enactor class. Takes rules from rule interpreter and assists game engine/view with implementing them.
	"""
	
			
	valid_dice_regex = "^[0-9]*d[0-9]+$"
	
	all_created_entities = []
	
	keywords = {}
				
	operators = {}
				
	#spaceless_operators = ["+", "-", "/", "*", "=", "==", "<", ">"]
				
	variables = {}
	
	targeted_point = None
	
	#targeted_entities = []
	
	targeted_entity = None
	
	acting_entity = None
	
	
	def __init__(self):
		self.selected_item = None
		
	def add_new_entity(self, entity):
		self.all_created_entities.append(entity)
				
	def _is_number(s):
		try: 
			float(s)
		except ValueError:
			return False
		return True
		
	def perform_action(self, written_rule, acting_entity):
		# ...
		# parse out the target type from the action (Entity or point)
		print("Rule:")
		print(written_rule)
		lines = written_rule.splitlines()
		print("got lines")
		print(lines)
		#set self here
		self.acting_entity = acting_entity
		# perform each line
		for line in lines:
			print("Evaluating line: " + line)
			print(self.evaluate_line(self, line))
		
	def evaluate_line(self, line):
		words = line.split()
		#base cases:
		# just a number
		if self._is_number(words[0]) and len(words) == 1:
			#print("Evaluator: Its a number!")
			return float(words[0])
		# a dice roll
		elif re.search(self.valid_dice_regex, words[0]) and len(words) == 1:
			#print("Evaluator: Its a dice roll!")
			return self.roll_dice(words[0])
		# calling a 'function' with a keyword
		elif words[0] in self.keywords:
			#print("Evaluator: Its a function!")
			return self.keywords[words[0]](self, line)
		#using an operator 
		# elif words[1] in self.operators:
			# print("Evaluator: Its an operator!")
			# return self.operators[words[1]](self, line)
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
			#print("Evaluator: Its an operator! (" + first_operator + ")")
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
			#print("Evaluator: Its an operator! (" + first_operator + ")")
			return self.operators[first_operator](self, line)
		# might be an attribute of the targeted entity
		entity_attribute = line.split('.')
		if len(entity_attribute) > 1:
			for attr in self.targeted_entity.attributes:
				if attr.name == entity_attribute[1]:
					return attr.value
		
		
		# something else (a variable)
		if not self._is_number(words[0]) and len(words) == 1:
			#print("Evaluator: Its a variable!")
			return self.variables[words[0]]
		
		
	def handle_target(self, line):
		words = line.split()
		target_type = words[1]
		# they can either be targeting a point or an entity
		#point case:
		#TODO: we need to be calling a GUI function to give us a point. For now, this is hard coded in. 
		if words[1] == 'point':
			targeted_point = (1,1)
		# entity case:
		#TODO: in reality we need to be calling a GUI function that gives us the targeted entity...
		#thus this is a placeholder for now
		else:
			for entity in self.all_created_entities:
				if entity.type == target_type:
					self.targeted_entity = entity
		
		
	def handle_if(self, line):
		#TODO
		post_if = line.split('if')[1].strip()
		print(post_if)
		conditional_and_action = post_if.split('then')
		print(conditional_and_action)
		conditional = conditional_and_action[0].strip()
		action = conditional_and_action[1].strip()
		
		if self.evaluate_line(self, conditional):
			return self.evaluate_line(self, action)
	
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
			self.variables[words[1]] += self.evaluate_line(self, " ".join(rest_of_sentence))
		# must be increasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value += self.evaluate_line(self, " ".join(rest_of_sentence))
			#targeting target entity
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value += self.evaluate_line(self, " ".join(rest_of_sentence))
				
		
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
			self.variables[words[1]] -= self.evaluate_line(self, " ".join(rest_of_sentence))
		# must be decreasing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value -= self.evaluate_line(self, " ".join(rest_of_sentence))
			#targeting target entity
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value -= self.evaluate_line(self, " ".join(rest_of_sentence))
		
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
			self.variables[words[1]] *= self.evaluate_line(self, " ".join(rest_of_sentence))
		# must be multiplying entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value *= self.evaluate_line(self, " ".join(rest_of_sentence))
			#targeting target entity
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value *= self.evaluate_line(self, " ".join(rest_of_sentence))
		
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
			self.variables[words[1]] /= self.evaluate_line(self, " ".join(rest_of_sentence))
		# must be dividing entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value /= self.evaluate_line(self, " ".join(rest_of_sentence))
			#targeting target entity
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value /= self.evaluate_line(self, " ".join(rest_of_sentence))
		
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
		if words[1] in self.variables:
			self.variables[words[1]] = self.evaluate_line(self, " ".join(rest_of_sentence))
		# must be setting entity
		else:
			entity_info = words[1].split('.')
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value = self.evaluate_line(self, " ".join(rest_of_sentence))
			#targeting target entity
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value = self.evaluate_line(self, " ".join(rest_of_sentence))
		
	def handle_within(self, written_rule):
		#TODO
		# handle detecting entities within a given distance of the selection
		print("within...")
		return
		
	def handle_moveaway(self, written_rule):
		#TODO
		# handle moving targets away from a given point or entity
		print("moveaway...")
		return
		
	def handle_movetowards(self, written_rule):
		#TODO
		# handle moving targets towards a given point or entity
		print("movetowards...")
		return
		
	def handle_plus(self, written_rule):
		words = written_rule.split('+')
		return self.evaluate_line(self, words[0].strip()) + self.evaluate_line(self, words[1].strip())
		
	def handle_minus(self, written_rule):
		words = written_rule.split('-')
		return self.evaluate_line(self, words[0].strip()) - self.evaluate_line(self, words[1].strip())
		
	def handle_equals(self, written_rule):
		words = written_rule.split('==')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) == self.evaluate_line(self, words[1].strip())
		words = written_rule.split('equals')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) == self.evaluate_line(self, words[1].strip())
		
	def handle_less_than(self, written_rule):
		words = written_rule.split('<')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) < self.evaluate_line(self, words[1].strip())
		words = written_rule.split('less than')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) < self.evaluate_line(self, words[1].strip())
		
	def handle_greater_than(self, written_rule):
		words = written_rule.split('>')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) > self.evaluate_line(self, words[1].strip())
		words = written_rule.split('greater than')
		if len(words) > 1:
			return self.evaluate_line(self, words[0].strip()) > self.evaluate_line(self, words[1].strip())
		
	def handle_multiply_operator(self, written_rule):
		words = written_rule.split('*')
		return self.evaluate_line(self, words[0].strip()) * self.evaluate_line(self, words[1].strip())
		
	def handle_divide_operator(self, written_rule):
		words = written_rule.split('/')
		return self.evaluate_line(self, words[0].strip()) / self.evaluate_line(self, words[1].strip())
		
	def handle_assignment(self, written_rule):
		words = written_rule.split('=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value = self.evaluate_line(self, " ".join(rest_of_sentence))
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value = self.evaluate_line(self, words[1].strip())
		else:
			self.variables[words[0].strip()] = self.evaluate_line(self, words[1].strip())
		
	def handle_plus_equals(self, written_rule):
		words = written_rule.split('+=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value += self.evaluate_line(self, " ".join(rest_of_sentence))
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value += self.evaluate_line(self, words[1].strip())
		else:
			self.variables[words[0].strip()] += self.evaluate_line(self, words[1].strip())
		
	def handle_minus_equals(self, written_rule):
		words = written_rule.split('-=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value -= self.evaluate_line(self, " ".join(rest_of_sentence))
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value -= self.evaluate_line(self, words[1].strip())
		else:
			self.variables[words[0].strip()] -= self.evaluate_line(self, words[1].strip())
	
	def handle_times_equals(self, written_rule):
		words = written_rule.split('*=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value *= self.evaluate_line(self, " ".join(rest_of_sentence))
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value *= self.evaluate_line(self, words[1].strip())
		else:
			self.variables[words[0].strip()] *= self.evaluate_line(self, words[1].strip())
			
	def handle_divide_equals(self, written_rule):
		words = written_rule.split('/=')
		
		entity_info = words[0].strip().split('.')
		if len(entity_info) > 1:
			if entity_info[0] == 'self':
				for attribute in self.acting_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value /= self.evaluate_line(self, " ".join(rest_of_sentence))
			else:
				for attribute in self.targeted_entity.attributes:
					if attribute.name == entity_info[1]:
						attribute.value /= self.evaluate_line(self, words[1].strip())
		else:
			self.variables[words[0].strip()] /= self.evaluate_line(self, words[1].strip())
	
	def handle_and(self, written_rule):
		words = written_rule.split('and')
		return self.evaluate_line(self, words[0].strip()) and self.evaluate_line(self, words[1].strip())
		
	def handle_or(self, written_rule):
		words = written_rule.split('or')
		return self.evaluate_line(self, words[0].strip()) or self.evaluate_line(self, words[1].strip())
	
	def roll_dice(dice_string):
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
				"towards":handle_movetowards, "away":handle_moveaway}
				
	combined_operators = {"+=":handle_plus_equals, "-=":handle_minus_equals, 
				"*=":handle_times_equals, "/=":handle_divide_equals, "==":handle_equals,}
				
	operators = {"within":handle_within, "+": handle_plus, "-":handle_minus,  
				"equals":handle_equals, "<":handle_less_than, ">":handle_greater_than, 
				"less":handle_less_than, "greater": handle_greater_than, "*": handle_multiply_operator,
				"/":handle_divide_operator, "=":handle_assignment, "and":handle_and, "or":handle_or}