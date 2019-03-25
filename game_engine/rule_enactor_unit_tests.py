import unittest
import rule_enactor
import sys
sys.path.append('../rule_interpreter/models')
from entity import Entity
from action import Action
from attribute import Attribute
from relationship import Relationship
from size import Size
from point import Point

class TestRuleInterpreter(unittest.TestCase):
	def setUp(self):
		self.action_name = "Action"
		debug_mode = True
		self.enactor = rule_enactor.RuleEnactor(debug_mode)

		self.rule = "target guy\n"
		self.isTemplate = False
		self.hp_time = rule_enactor.Attribute("HP", 10)	
		self.actor = rule_enactor.Entity("entity", "self", self.isTemplate)
		self.actor.add_attribute(self.hp_time)
	
		self.hp_boys = rule_enactor.Attribute("HP", 20)
		self.target = rule_enactor.Entity("entity", "guy", self.isTemplate)
		self.target.add_attribute(self.hp_boys)
		self.target.x = 2
		self.target.y = 2
		self.ac_time = rule_enactor.Attribute("AC", 15)	
		self.actor.add_attribute(self.ac_time)
	
		self.ac_boys = rule_enactor.Attribute("AC", 15)
		self.target.add_attribute(self.ac_boys)
	
		self.enactor.add_new_entity(self.actor)
		self.enactor.add_new_entity(self.target)
		
	# def tearDown(self):
		# print("Done test.")
	
	
	def test_constructor(self):
		newEnactor = rule_enactor.RuleEnactor()
		self.assertTrue(isinstance(newEnactor, rule_enactor.RuleEnactor))
	
	def test_add_new_entity(self):
		newEntity = rule_enactor.Entity("entity", "newGuy", self.isTemplate)
		self.enactor.add_new_entity(newEntity)
		self.assertTrue(newEntity in self.enactor.all_created_entities)
	
	def test_target(self):
		rule = "target guy\n"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.target_of_action, self.target)
		rule = "target self\n"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.target_of_action, self.actor)
	
	def test_initialize_variable(self):
		self.rule += "x = 0\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 0)
	
	def test_increase(self):
		self.rule += "x = 0\n"
		self.rule += "increase x by 4\n"
		self.rule += "increase target.HP by 5"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 25)
		
	def test_decrease(self):
		self.rule += "x = 0\n"
		self.rule += "decrease x by 4\n"
		self.rule += "decrease target.HP by 5"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], -4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 15)
		
	def test_multiply(self):
		self.rule += "x = 2\n"
		self.rule += "multiply x by 4\n"
		self.rule += "multiply target.HP by 2"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 8)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 40)
		
	def test_divide(self):
		self.rule += "x = 40\n"
		self.rule += "divide x by 4\n"
		self.rule += "divide target.HP by 5"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 4)
		
	def test_set(self):
		self.rule += "set x to 4\n"
		self.rule += "set target.HP to 5"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 5)
		
	def test_within(self):
		# actor is at 0,0
		# target is at 2,2
		# entity1 is at 1,1
		# entity2 is at 10,10
		# entity3 is at -3,-3 but has width and height of 3 so should be within
		hp_1 = rule_enactor.Attribute("HP", 10)
		entity1 = rule_enactor.Entity("entity", "entity1", self.isTemplate)
		entity1.add_attribute(hp_1)
		entity1.x = 1
		entity1.y = 1
		
		hp_2 = rule_enactor.Attribute("HP", 10)
		entity2 = rule_enactor.Entity("entity", "entity2", self.isTemplate)
		entity2.add_attribute(hp_2)
		entity2.x = 10
		entity2.y = 10
		
		hp_3 = rule_enactor.Attribute("HP", 10)
		entity3 = rule_enactor.Entity("entity", "entity3", self.isTemplate)
		entity3.add_attribute(hp_3)
		entity3.x = -3
		entity3.y = -3
		entity3.set_size(rule_enactor.Size(3,3))
		
		self.enactor.add_new_entity(entity1)
		self.enactor.add_new_entity(entity2)
		self.enactor.add_new_entity(entity3)
		#print("target hp: " + str(self.target.get_attribute("HP").get_attribute_value()))
		self.rule += "if all self within(2,2) of entity then reduce entity.HP by 5\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		#self hp should be 5
		self.assertEqual(self.enactor.acting_entity.get_attribute("HP").get_attribute_value(), 5)
		#entity1 hp should be 5
		self.assertEqual(self.enactor.get_entity("entity1").get_attribute("HP").get_attribute_value(), 5)
		#entity2 hp should be 10
		self.assertEqual(self.enactor.get_entity("entity2").get_attribute("HP").get_attribute_value(), 10)
		#entity3 HP should be 5
		self.assertEqual(self.enactor.get_entity("entity3").get_attribute("HP").get_attribute_value(), 5)
		#target hp should be 15
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 15)
		
	def test_if(self):
		self.rule += "x = 9\n"
		self.rule += "if x equals 9 then increase target.HP by 10\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		# HP should go up by 10
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 30)
		rule = "target guy\n x = 6\n if x equals 9 then increase target.HP by 10\n"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		#HP should not change
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 30)
		
	def test_moveaway(self):
		self.target.x = 0
		self.target.y = 5
		self.rule += "move target 3 away from self\n"
		self.rule += "move self 3 away from target\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.target.x, 0)
		self.assertEqual(self.target.y, 8)
		self.assertEqual(self.actor.x, 0)
		self.assertEqual(self.actor.y, -3)
		
		entity1 = rule_enactor.Entity("entity", "test1", self.isTemplate)
		entity1.x = 5
		entity1.y = 0
		self.enactor.add_new_entity(entity1)
		rule = "target test1\n move target 10 away from self\nmove self 10 away from target"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(entity1.x, 15)
		self.assertEqual(entity1.y, 0)
		self.assertEqual(self.actor.x, -10)
		self.assertEqual(self.actor.y, -3)
		
		rule = "target point\n move self 3 away from target\n"
		#point is hard coded to be 1,1
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.actor.x, -13)
		self.assertEqual(self.actor.y, -3)
		
	def test_movetowards(self):
		self.target.x = 0
		self.target.y = 5
		self.rule += "move target 3 towards self\n"
		self.rule += "move self 3 towards target\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		# since they"re both moving 3 towards each other, they will meet at 2 rather than pass each other
		self.assertEqual(self.target.x, 0)
		self.assertEqual(self.target.y, 2)
		self.assertEqual(self.actor.x, 0)
		self.assertEqual(self.actor.y, 2)
		
		entity1 = rule_enactor.Entity("entity", "test1", self.isTemplate)
		entity1.x = 15
		entity1.y = 0
		self.enactor.add_new_entity(entity1)
		rule = "target test1\n move target 5 towards self\nmove self 10 towards target"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(entity1.x, 10)
		self.assertEqual(entity1.y, 0)
		self.assertEqual(self.actor.x, 10)
		self.assertEqual(self.actor.y, 2)
		
		rule = "target point\n move self 3 towards target\n"
		#point is hard coded to be 1,1
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.actor.x, 7)
		self.assertEqual(self.actor.y, 2)
		
	def tast_plus(self):
		self.rule += "x = 0\n"
		self.rule += "x = 5 + 5\n"
		self.rule += "y = x + 4\n"
		self.rule += "target.HP = y + 1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.variables["y"], 14)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP"), 15)
		
	def test_minus(self):
		self.rule += "x = 0\n"
		self.rule += "x = 5 - 5\n"
		self.rule += "y = x - 4\n"
		self.rule += "target.HP = 15 - 1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 0)
		self.assertEqual(self.enactor.variables["y"], -4)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 14)
		
	def test_equals(self):
		self.rule += "x = 0\n"
		self.rule += "y = 0\n"
		self.rule += "if x equals y then yeet = 9\n"
		self.rule += "if x == y then yote = 9\n"
		self.rule += "if x equals 999 then yeet = 333\n"
		self.rule += "if x == 9999 then yote = 333\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["yeet"], 9)
		self.assertEqual(self.enactor.variables["yote"], 9)
		
	def test_less_than(self):
		self.rule += "x = 10\n"
		self.rule += "y = 19\n"
		self.rule += "if x < y then xless = 1\n"
		self.rule += "if y < 999 then yless = 1\n"
		self.rule += "if y < x then xless = 0\n"
		self.rule += "if y < 1 then yless = 0\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["xless"], 1)
		self.assertEqual(self.enactor.variables["yless"], 1)
		
	def test_less_than(self):
		self.rule += "x = 10\n"
		self.rule += "y = 19\n"
		self.rule += "if x > y then xless = 1\n"
		self.rule += "if y > 999 then yless = 1\n"
		self.rule += "if y > x then xless = 0\n"
		self.rule += "if y > 1 + 1 then yless = 0\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["xless"], 0)
		self.assertEqual(self.enactor.variables["yless"], 0)
		
	def test_multiply_operator(self):
		self.rule += "x = 5 * 5\n"
		self.rule += "y = x * 0.2\n"
		self.rule += "z = y * -1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 25)
		self.assertEqual(self.enactor.variables["y"], 5)
		self.assertEqual(self.enactor.variables["z"], -5)
	
	def test_divide_operator(self):
		self.rule += "x = 5 / 5\n"
		self.rule += "y = x / 0.2\n"
		self.rule += "z = y / -1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 1)
		self.assertEqual(self.enactor.variables["y"], 5)
		self.assertEqual(self.enactor.variables["z"], -5)
		
	def test_assignment(self):
		self.rule += "x = 5\n"
		self.rule += "target.HP = 5\n"
		self.rule += "str = \"Literal\"\n"
		self.rule += "bool1 = True\n"
		self.rule += "bool2 = False\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 5)
		self.assertEqual(self.enactor.variables["str"], "literal")
		self.assertEqual(self.enactor.variables["bool1"], True)
		self.assertEqual(self.enactor.variables["bool2"], False)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 5)
		
	def test_plus_equals(self):
		self.rule += "x = 0\n"
		self.rule += "x += 10\n"
		self.rule += "y = 0\n"
		self.rule += "y += x + 1\n"
		self.rule += "target.HP += 1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.variables["y"], 11)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 21)
	
	def test_minus_equals(self):
		self.rule += "x = 0\n"
		self.rule += "x -= 10\n"
		self.rule += "y = 0\n"
		self.rule += "y -= x + 1\n"
		self.rule += "target.HP -= 1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], -10)
		self.assertEqual(self.enactor.variables["y"], 9)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 19)
		
	def test_times_equals(self):
		self.rule += "x = 1\n"
		self.rule += "x *= 10\n"
		self.rule += "y = 1\n"
		self.rule += "y *= x * 2\n"
		self.rule += "target.HP *= 0.1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 10)
		self.assertEqual(self.enactor.variables["y"], 20)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 2)
		
	def test_divide_equals(self):
		self.rule += "x = 10\n"
		self.rule += "x /= 2\n"
		self.rule += "y = 900\n"
		self.rule += "y /= x\n"
		self.rule += "target.HP /= 2\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["x"], 5)
		self.assertEqual(self.enactor.variables["y"], 180)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 10)
		
	def test_and(self):
		self.rule += "x = 10\n"
		self.rule += "if x equals 10 and x < 100 then yeet = 1\n"
		self.rule += "if x equals 10 and x > 100 then yeet = 0\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["yeet"], 1)
		
		
	def test_or(self):
		self.rule += "x = 10\n"
		self.rule += "y = 5\n"
		self.rule += "if x equals 10 or x < 100 then yeet = 1\n"
		self.rule += "if y equals 5 or x > 100 then yeet2 = 1\n"
		self.rule += "if y less than 5 or x < 100 then yeet3 = 1\n"
		self.rule += "if y equals 999 or x equals 100 then yeet3 = 0\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["yeet"], 1)
		self.assertEqual(self.enactor.variables["yeet2"], 1)
		self.assertEqual(self.enactor.variables["yeet3"], 1)
		
	def test_roll_dice(self):
		self.rule += "x = d20\n"
		self.rule += "y = 1d20\n"
		self.rule += "z = 5d6\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertTrue(1 <= self.enactor.variables["x"] and self.enactor.variables["x"] <= 20)
		self.assertTrue(1 <= self.enactor.variables["y"] and self.enactor.variables["y"] <= 20)
		self.assertTrue(5 <= self.enactor.variables["z"] and self.enactor.variables["z"] <= 30)
		
	def test_add_status(self):
		self.rule += "add status \"Dodge\" to self\n"
		self.rule += "add status Poisoned to self\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertTrue("dodge" in self.enactor.acting_entity.get_current_statuses())
		self.assertTrue("poisoned" in self.enactor.acting_entity.get_current_statuses())
	
	def test_remove_status(self):
		self.rule += "add status \"Dodge\" to self\n"
		self.rule += "add status Poisoned to self\n"
		self.rule += "remove status Dodge from self\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertTrue("dodge" not in self.enactor.acting_entity.get_current_statuses())
		self.assertTrue("poisoned" in self.enactor.acting_entity.get_current_statuses())
	
	def test_has_status(self):
		self.rule += "add status Poisoned to self\n"
		self.rule += "if self.statuses has Poisoned then yeet = 1\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.variables["yeet"],1)
		
	def test_interrupt(self):
		relationship_rule = "interrupt entity.Action if target.statuses has \"Dodge\"\nincrease target.HP by 10\n"
		relationship = rule_enactor.Relationship(relationship_rule)
		self.rule += "add status \"Dodge\" to target"
		action = rule_enactor.Action("Setup", self.rule)
		self.enactor.perform_action(action, self.actor)
		self.enactor.add_new_relationship(relationship)
		rule = "target guy \n reduce target.HP by 10\n"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 30)
		
	def test_attack_action(self):
		self.rule += "roll = d20\n"
		self.rule += "if roll > target.AC then reduce target.HP by 1d8\n"
		action = rule_enactor.Action(self.action_name, self.rule)
		self.enactor.perform_action(action, self.actor)
		if self.enactor.variables["roll"] > 15:
			self.assertTrue(self.enactor.target_of_action.get_attribute("HP").get_attribute_value() < 20 and self.enactor.target_of_action.get_attribute("HP").get_attribute_value() > 11)
		else:
			self.assertEqual(self.enactor.target_of_action.get_attribute("HP").get_attribute_value(), 20)
		
		
	def test_fireball_action(self):
		rule = "target point:\n"
		rule += "if all entity within(3, 3) of target and d20 > self.AC then reduce entity.HP by 6d6\n"
		action = rule_enactor.Action(self.action_name, rule)
		self.enactor.perform_action(action, self.actor)
		self.assertTrue(self.target.get_attribute("HP").get_attribute_value() <= 20 and self.target.get_attribute("HP").get_attribute_value() >= -16)
		self.assertTrue(self.enactor.acting_entity.get_attribute("HP").get_attribute_value() <= 10 and self.enactor.acting_entity.get_attribute("HP").get_attribute_value() >= -26)
		
	#ETC ETC (test complex and concrete examples of actions)


if __name__=="__main__":
	unittest.main()