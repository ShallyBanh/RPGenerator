import unittest
import rule_enactor


class TestRuleInterpreter(unittest.TestCase):
	def setUp(self):
		self.enactor = rule_enactor.RuleEnactor()

		self.rule = "target guy\n"

		self.hp_time = rule_enactor.Attribute("HP", 10)	
		self.actor = rule_enactor.Entity("self", "entity")
		self.actor.add_attribute(self.hp_time)
	
		self.hp_boys = rule_enactor.Attribute("HP", 20)
		self.target = rule_enactor.Entity("guy", "entity")
		self.target.add_attribute(self.hp_boys)
		self.target.x = 2
		self.target.y = 2
	
		self.enactor.add_new_entity(self.actor)
		self.enactor.add_new_entity(self.target)
		
	# def tearDown(self):
		# print("Done test.")
	
	
	def test_constructor(self):
		newEnactor = rule_enactor.RuleEnactor()
		self.assertTrue(isinstance(newEnactor, rule_enactor.RuleEnactor))
	
	def test_add_new_entity(self):
		newEntity = rule_enactor.Entity("newGuy", "entity")
		self.enactor.add_new_entity(newEntity)
		self.assertTrue(newEntity in self.enactor.all_created_entities)
	
	def test_target(self):
		rule = "target guy\n"
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(self.enactor.target_of_action, self.target)
		rule = "target self\n"
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(self.enactor.target_of_action, self.actor)
	
	def test_initialize_variable(self):
		self.rule += "x = 0\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 0)
	
	def test_increase(self):
		self.rule += "x = 0\n"
		self.rule += "increase x by 4\n"
		self.rule += "increase target.HP by 5"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 25)
		
	def test_decrease(self):
		self.rule += "x = 0\n"
		self.rule += "decrease x by 4\n"
		self.rule += "decrease target.HP by 5"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], -4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 15)
		
	def test_multiply(self):
		self.rule += "x = 2\n"
		self.rule += "multiply x by 4\n"
		self.rule += "multiply target.HP by 2"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 8)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 40)
		
	def test_divide(self):
		self.rule += "x = 40\n"
		self.rule += "divide x by 4\n"
		self.rule += "divide target.HP by 5"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 4)
		
	def test_set(self):
		self.rule += "set x to 4\n"
		self.rule += "set target.HP to 5"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 5)
		
	def test_within(self):
		# actor is at 0,0
		# target is at 2,2
		# entity1 is at 1,1
		# entity2 is at 10,10
		hp_1 = rule_enactor.Attribute("HP", 10)
		entity1 = rule_enactor.Entity("entity1", "entity")
		entity1.add_attribute(hp_1)
		entity1.x = 1
		entity1.y = 1
		
		hp_2 = rule_enactor.Attribute("HP", 10)
		entity2 = rule_enactor.Entity("entity2", "entity")
		entity2.add_attribute(hp_2)
		entity2.x = 10
		entity2.y = 10
		
		self.enactor.add_new_entity(entity1)
		self.enactor.add_new_entity(entity2)
		#print("target hp: " + str(self.target.get_attribute("HP").value))
		self.rule += "if all self within(2,2) of entity then reduce entity.HP by 5\n"
		self.enactor.perform_action(self.rule, self.actor)
		#self hp should be 5
		self.assertEqual(self.enactor.acting_entity.get_attribute("HP").value, 5)
		#entity1 hp should be 5
		self.assertEqual(self.enactor.get_entity("entity1").get_attribute("HP").value, 5)
		#entity2 hp should be 10
		self.assertEqual(self.enactor.get_entity("entity2").get_attribute("HP").value, 10)
		#target hp should be 15
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 15)
		
	def test_on(self):
		pass #TODO
		
	def test_if(self):
		self.rule += "x = 9\n"
		self.rule += "if x equals 9 then increase target.HP by 10\n"
		self.enactor.perform_action(self.rule, self.actor)
		# HP should go up by 10
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 30)
		rule = "target guy\n x = 6\n if x equals 9 then increase target.HP by 10\n"
		self.enactor.perform_action(rule, self.actor)
		#HP should not change
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 30)
		
	def test_moveaway(self):
		self.target.x = 0
		self.target.y = 5
		self.rule += "move target 3 away from self\n"
		self.rule += "move self 3 away from target\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.target.x, 0)
		self.assertEqual(self.target.y, 8)
		self.assertEqual(self.actor.x, 0)
		self.assertEqual(self.actor.y, -3)
		
		entity1 = rule_enactor.Entity("test1","entity")
		entity1.x = 5
		entity1.y = 0
		self.enactor.add_new_entity(entity1)
		rule = "target test1\n move target 10 away from self\nmove self 10 away from target"
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(entity1.x, 15)
		self.assertEqual(entity1.y, 0)
		self.assertEqual(self.actor.x, -10)
		self.assertEqual(self.actor.y, -3)
		
		rule = "target point\n move self 3 away from target\n"
		#point is hard coded to be 1,1
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(self.actor.x, -13)
		self.assertEqual(self.actor.y, -3)
		
	def test_movetowards(self):
		self.target.x = 0
		self.target.y = 5
		self.rule += "move target 3 towards self\n"
		self.rule += "move self 3 towards target\n"
		self.enactor.perform_action(self.rule, self.actor)
		# since they"re both moving 3 towards each other, they will meet at 2 rather than pass each other
		self.assertEqual(self.target.x, 0)
		self.assertEqual(self.target.y, 2)
		self.assertEqual(self.actor.x, 0)
		self.assertEqual(self.actor.y, 2)
		
		entity1 = rule_enactor.Entity("test1","entity")
		entity1.x = 15
		entity1.y = 0
		self.enactor.add_new_entity(entity1)
		rule = "target test1\n move target 5 towards self\nmove self 10 towards target"
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(entity1.x, 10)
		self.assertEqual(entity1.y, 0)
		self.assertEqual(self.actor.x, 10)
		self.assertEqual(self.actor.y, 2)
		
		rule = "target point\n move self 3 towards target\n"
		#point is hard coded to be 1,1
		self.enactor.perform_action(rule, self.actor)
		self.assertEqual(self.actor.x, 7)
		self.assertEqual(self.actor.y, 2)
		
	def tast_plus(self):
		self.rule += "x = 0\n"
		self.rule += "x = 5 + 5\n"
		self.rule += "y = x + 4\n"
		self.rule += "target.HP = y + 1\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.variables["y"], 14)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP"), 15)
		
	def test_minus(self):
		self.rule += "x = 0\n"
		self.rule += "x = 5 - 5\n"
		self.rule += "y = x - 4\n"
		self.rule += "target.HP = 15 - 1\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["x"], 0)
		self.assertEqual(self.enactor.variables["y"], -4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").value, 14)
		
	def test_equals(self):
		self.rule += "x = 0\n"
		self.rule += "y = 0\n"
		self.rule += "if x equals y then yeet = 9\n"
		self.rule += "if x == y then yote = 9\n"
		self.rule += "if x equals 999 then yeet = 333\n"
		self.rule += "if x == 9999 then yote = 333\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["yeet"], 9)
		self.assertEqual(self.enactor.variables["yote"], 9)
		
	def test_less_than(self):
		self.rule += "x = 10\n"
		self.rule += "y = 19\n"
		self.rule += "if x < y then xless = 1\n"
		self.rule += "if y < 999 then yless = 1\n"
		self.rule += "if y < x then xless = 0\n"
		self.rule += "if y < 1 then yless = 0\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["xless"], 1)
		self.assertEqual(self.enactor.variables["yless"], 1)
		
	def test_less_than(self):
		self.rule += "x = 10\n"
		self.rule += "y = 19\n"
		self.rule += "if x > y then xless = 1\n"
		self.rule += "if y > 999 then yless = 1\n"
		self.rule += "if y > x then xless = 0\n"
		self.rule += "if y > 1 then yless = 0\n"
		self.enactor.perform_action(self.rule, self.actor)
		self.assertEqual(self.enactor.variables["xless"], 0)
		self.assertEqual(self.enactor.variables["yless"], 0)
		
	def test_multiply_operator(self):
		pass #TODO
	
	def test_divide_operator(self):
		pass #TODO
		
	def test_assignment(self):
		pass #TODO
		
	def test_plus_equals(self):
		pass #TODO
	
	def test_minus_equals(self):
		pass #TODO
		
	def test_times_equals(self):
		pass #TODO
		
	def test_divide_equals(self):
		pass #TODO
		
	def test_and(self):
		pass #TODO
		
	def test_or(self):
		pass #TODO
		
	def test_roll_dict(self):
		pass #TODO
		
	def test_attack_action(self):
		pass #TODO
		
	def test_fireball_action(self):
		pass #TODO
		
	#ETC ETC


if __name__=="__main__":
	unittest.main()