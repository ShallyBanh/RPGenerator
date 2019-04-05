"""
This file contains unit tests for the rule_interpreter syntax parser
"""
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
        goblin = Entity("steve", "goblin", 1, 1, "no", None)
        testAttribute = Attribute("hp", 1)
        testAttribute2 = Attribute("cool", 2)
        testAttribute3 = Attribute("strength", 3)
        goblin.add_attribute(testAttribute)
        goblin.add_attribute(testAttribute2)
        goblin.add_attribute(testAttribute3)
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
    
    def test_reduce_action_by_10d10(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n reduce goblin.HP by 10d10"))

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

    def test_multiply_action_to_self(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n multiply self.HP to 5"))

    def test_multiply_action_to_target(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n multiply target.HP to 5"))

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
    
    def test_andrews_test_1(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 0"))

    def test_andrews_test_2(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 0\n increase x by 4\n increase target.hp by 4"))

    def test_andrews_test_3(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 0\n decrease x by 4\n decrease target.hp by 4"))

    def test_andrews_test_4(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 1\n multiply x by 4\n multiply target.hp by 4"))

    def test_andrews_test_5(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 4\n divide x by 4\n divide target.hp by 2"))

    def test_andrews_test_6(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n set x to 4\n set target.hp to 8"))

    def test_andrews_test_7(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n if all self within(2,2) of goblin then reduce goblin.hp by 5"))

    def test_andrews_test_8(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 9\n if x equals 9 then increase target.hp by 10\n if x == 9 then increase target.hp by 2"))

    def test_andrews_test_9(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n move target 3 away from self\n move self 3 away from target"))

    def test_andrews_test_10(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n move target 3 towards self\n move self 3 towards target"))

    def test_andrews_test_11(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 0\n y = x + 4\n target.hp = y + 1"))
    
    def test_andrews_test_12(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 10\n y = 19\n if x < y then reduce target.hp by x\n if x less than y then reduce target.hp by y"))

    def test_andrews_test_13(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 10\n y = 19\n if y > x then increase target.hp by x\n if y greater than x then increase target.hp by y"))

    def test_andrews_test_14(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 1\n y = 2\n x = x * 2\n y = y / 2\n if x equals 2 then target.hp = 9\n if y equals 1 then increase target.hp by 11"))

    def test_andrews_test_15(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = 1\n y = 2\n z = 3\n a = 4\n x += 2\n y -= 2\n z *= 3\n a /= 4"))

    def test_andrews_test_16(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n if 1 equals 1 and 2 equals 2 then increase target.hp by 2\n if 2 equals 100 or 8 equals 8 then increase target.hp by 17"))
    
    def test_andrews_test_17(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n x = d20"))

    def test_andrews_test_18(self):
        self.assertTrue(self.parser.is_valid_rule("target self:\n add status \"Dodge\" to self\n remove status \"Dodge\" from self\n if target.statuses has \"Dodge\" then reduce target.hp by 100"))

    def test_andrews_test_19(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt entity.attack if target.statuses has \"Dodge\":\n increase target.hp by 10"))

    def test_andrews_test_20(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\n roll = d20\n if roll > target.hp then reduce target.hp by 1d8"))

    def test_andrews_test_21(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if all entity within(3,3) of target and d20 > entity.hp then reduce entity.hp by 6d6"))

    def test_andrews_test_22(self):
        self.assertTrue(self.parser.is_valid_rule("target Parent:\n reduce target.HP by self.hp"))

    def test_andrews_test_23(self):
        self.assertTrue(self.parser.is_valid_rule("target goblin:\nif target.hp < self.Strength + d20 then reduce target.HP by 1d4 + self.Strength"))

if __name__ == '__main__':
    unittest.main()
 
    # parser = SyntaxParser()

    # goblin = Entity("steve", "goblin", 1, 1, "no", None)
    # testAttribute = Attribute("hp", 1)
    # goblin.add_attribute(testAttribute)
    # testAttribute = Attribute("strength", 1)
    # goblin.add_attribute(testAttribute)
    # testAction = Action("Attack", "target goblin:\n if goblin.hp > 2 then 2")
    # goblin.add_action(testAction)
    # goblin.add_status("Dodge")
    # Validator().add_entity(goblin)

    # print(parser.is_valid_rule("""target goblin:\nif target.hp < self.Strength + d20 then reduce target.HP by 1d4 + self.Strength"""))