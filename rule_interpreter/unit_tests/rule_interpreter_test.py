import unittest
import os
import sys
sys.path.append('../models')
from validator import Validator
from entity import Entity
from action import Action
from attribute import Attribute
from syntax_parser import SyntaxParser



class TestValidator(unittest.TestCase):
    def setUp(self):
        self.parser = SyntaxParser()
        goblin = Entity("steve", "goblin", 1, 1, "no", "no")
        testAttribute = Attribute("hp", 1)
        testAttribute2 = Attribute("cool", 2)
        goblin.add_attribute(testAttribute)
        goblin.add_attribute(testAttribute2)
        testAction = Action("Attack", "target goblin:\n if goblin.hp > 2 then 2")
        goblin.add_action(testAction)
        goblin.add_status("Dodge")
        Validator().add_entity(goblin)

    def test_target_entity_false(self):
        self.assertFalse(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then 2"""))
        
    def test_target_entity_true(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then goblin.hp = 2"""))
    
    def test_target_entity_two_entities(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then goblin.cool += 2"""))

    def test_target_entity_add_status(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then add status \"od\" to goblin"""))
    
    def test_target_entity_action_statement_only(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n add status \"dodge\" to goblin"""))
    
    def test_target_point(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if entity within(3,3) of point then goblin.hp = 2"))
    
    def test_target_point_single_digit(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if entity within(3) of point then goblin.hp = 2"))
    
    def test_target_point_all_keyword(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if all entity  within(3,3) of point then goblin.hp = 2"))
    
    def test_target_point_false(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n If entity within(3) of target then move entity 1 away from target"))
    
    def test_pull_action(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n move target 1 towards self"))
    
    def test_push_action(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n move target 1 away from self"))

    def test_increase_action_by(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n increase goblin.HP by 5"))

    def test_increase_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n increase goblin.HP to 5"))

    def test_reduce_action_by(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n reduce goblin.HP by 5"))

    def test_reduce_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n reduce goblin.HP to 5"))

    def test_decrease_action_by(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n decrease goblin.HP by 5"))

    def test_decrease_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n decrease goblin.HP to 5"))

    def test_set_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n set goblin.HP to 5"))

    def test_set_variable_using_set_keyword(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n set x to 5"))
    
    def test_set_attribute_variable_using_set_keyword(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n set goblin.hp to 5"))
    
    def test_set_action_by(self):
        self.assertFalse(self.parser.is_valid_rule("target goblin:\n set goblin.HP by 5"))

    def test_multiply_action_by(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n multiply goblin.HP by 5"))

    def test_multiply_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n multiply goblin.HP to 5"))

    def test_divide_action_by(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n divide goblin.HP by 5"))

    def test_divide_action_to(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n divide goblin.HP to 5"))
    
    def test_arithmetic_multiply(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n goblin.HP = 5 * 5"))
    
    def test_arithmetic_add(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n goblin.HP = 5 + 5"))
    
    def test_arithmetic_subtract(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n goblin.HP = 5 - 5"))

    def test_arithmetic_divide(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n goblin.HP = 5/5"))
    
    def test_explosion_action(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n If entity within(3) of point then move entity 1 away from target"))

    def test_target_interrupt(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n target.hp = 3"))
    
    def test_interrupt_contains_statuses(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.statuses contains  \"dodge\":\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll1 = roll2"))
    
    def test_variable_assignment(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll2 = roll2"))

if __name__ == '__main__':
    unittest.main()
 

    # parser = SyntaxParser()

    # goblin = Entity("steve", "goblin", 1, 1, "no", "no")
    # testAttribute = Attribute("hp", 1)
    # goblin.add_attribute(testAttribute)
    # testAction = Action("Attack", "")
    # goblin.add_action(testAction)
    # goblin.add_status("Dodge")
    # Validator().add_entity(goblin)

    # print(parser.is_valid_rule("""target goblin:\n goblin.HP = 5 * 5"""))