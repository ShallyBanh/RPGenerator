
class RuleEnactor:
	"""
	Rule Enactor class. Takes rules from rule interpreter and assists game engine/view with implementing them.
	"""
	
	keywords = {"target":handle_target, "if":handle_if, "else":handle_else, 
				"increase":handle_increase,"decrease":handle_decrease, "multiply":handle_multiply,
				"divide":handle_divide, "set":handle_set}
	
	def __init__(self):
		# something
		
	def perform_action(written_rule):
		# ...
		# parse out the target type from the action (Entity or point)
		words = written_rule.split()
		# recursively move through code and parse out action
		evaluate_rule(words)
		
	def evaluate_rule(words):
		#base case
		if _is_number(words[0]):
			return float(words[0])
		elif words[0] in keywords:
			return keywords[words[0]](words)
		
	def handle_target(written_rule):
		# handle targeting something
		
	def handle_if(written_rule):
		# handle if statement
		
	def handle_else(written_rule):
		# handle else statement?
	
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
	
	def _is_number(s):
		try: 
			float(s)
		except ValueError:
			return False
		return True
		