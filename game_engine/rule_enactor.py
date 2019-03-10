import re
import random

class RuleEnactor:
	"""
	Rule Enactor class. Takes rules from rule interpreter and assists game engine/view with implementing them.
	"""
	
	valid_dice_regex = "^[0-9]*d[0-9]+$"
	
	keywords = {"target":handle_target, "if":handle_if, "else":handle_else, 
				"increase":handle_increase,"decrease":handle_decrease, "multiply":handle_multiply,
				"divide":handle_divide, "set":handle_set, "within":handle_within, 
				"towards":handle_movetowards, "away":handle_moveaway}
				
	variables = {}
	
	selected_item = None
	
	def __init__(self):
		# something
		selected_item = None
		
	def perform_action(written_rule):
		# ...
		# parse out the target type from the action (Entity or point)
		lines = written_rule.splitlines()
		# perform each line
		for line in lines:
			evaluate_line(line)
		
	def evaluate_line(line):
		words = line[0].split()
		#base case
		if _is_number(words[0]) and len(words) == 1:
			return float(words[0])
		if re.search(valid_dice_regex, words[0]) and len(words) == 1:
			return roll_dice(words[0])
		elif words[0] in keywords:
			return keywords[words[0]](line)
		
	def handle_target(line):
		# handle targeting something
		words = line.split()
		# call game engine function to target a point or entity
		if words[1] == 'point':
			#target point
		else:
			#target entity
		# when this is resolved, set the selected item so it can be referenced later:
		selected_item = 999 #placeholder
		
	def handle_if(line):
		words = line.split()
		# handle if statement
		#for i in range(0,len(words)):
		#	if words[i] == 'then':
		#		break
		# index 1 to i - 1 is the conditional
		# index i + 1 to end is the statement to complete 
		
		then_idx = line.find('then')
		if_idx = line.find('if')
		# if_idx + 2 to then_idx is the conditional statement
		# then_idx + 4 to end is the statement to execute on true
	
	def handle_increase(written_rule):
		#handle increasing something
		
		
	def handle_decrease(written_rule):
		#handle decreasing something
		
		
	def handle_multiply(written_rule):
		#handle multiplying something
		
		
	def handle_divide(written_rule):
		#handle dividing something
		
		
	def handle_set(written_rule):
		#handle setting something
		
		
	def handle_within(written_rule):
		# handle detecting entities within a given distance of the selection
		
		
	def handle_moveaway(written_rule):
		# handle moving targets away from a given point or entity
		
		
	def handle_movetowards(written_rule):
		# handle moving targets towards a given point or entity
		
	
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
	
	def _is_number(s):
		try: 
			float(s)
		except ValueError:
			return False
		return True
		