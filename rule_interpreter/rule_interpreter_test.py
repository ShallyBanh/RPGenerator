import unittest
# from validator import Validator
# from entity import Entity
# from action import Action
# from attribute import Attribute
# from syntax_parser import SyntaxParser



class TestValidator(unittest.TestCase):
    def setUp(self):
        self.parser = SyntaxParser()
        goblin = Entity("goblin", "steve", 1)
        testAttribute = Attribute("hp", 1, 1)
        goblin.add_attribute(testAttribute)
        testAction = Action("Attack", 1)
        goblin.set_actions([testAction])
        goblin.add_status("Dodge")

    def test_target_entity_false(self):
        self.assertFalse(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then 2"""))
        
    def test_target_entity_true(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then goblin.hp = 2"""))
    
    def test_target_entity_add_status(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then add status \"od\" to goblin"""))
    
    def test_target_entity_action_statement_only(self):
        self.assertTrue(self.parser.is_valid_rule("""target goblin:\n add status \"dodge\" to goblin"""))
    
    def test_target_point(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if entity within(3,3) of point then goblin.hp = 2"))
    
    def test_target_point_single_digit(self):
        self.assertTrue(self.parser.is_valid_rule("target point:\n if entity within(3) of point then goblin.hp = 2"))

    def test_target_interrupt(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n target.hp = 3"))
    
    def test_interrupt_contains_statuses(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.statuses contains “Dodge”:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll1 = roll2"))
    
    def test_variable_assignment(self):
        self.assertTrue(self.parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll2 = roll2"))

if __name__ == '__main__':
    unittest.main()
 

    # parser = SyntaxParser()

    # print("Shally's dank test suite for the parser:\n")
    # print("adding entity goblin..")
    # goblin = Entity("goblin", "steve", 1)
    # print("adding atrributes for goblin: hp..")
    # testAttribute = Attribute("hp", 1, 1)
    # goblin.add_attribute(testAttribute)
    # print("adding actions for goblin: Attack..")
    # testAction = Action("Attack", 1)
    # goblin.add_action(testAction)
    # print("adding status for goblin: Dodge..")
    # goblin.add_status("Dodge")

    # print(parser.is_valid_rule("""interrupt goblin.Attack if target.hp equals 5:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll2 = roll2"""))


# print("Rule: ")
# print("target goblin:\n if goblin.hp > 2 then 2")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp then 2"""))


# print("\n\n\nRule: ")
# print("target goblin:\n if goblin.hp > 2 and goblin.hp > 2 then 2")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then 2"""))

# print("\n\n\nRule: ")
# print("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then add status \"dodge\" to goblin\n golbin.hp = 1""")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then add status \"dodge\" to goblin\n2 goblin.hp = 1"""))


# print("\n\n\nRule: ")
# print("""target goblin:\n add status \"dodge\" to goblin""")
#print(parser.is_valid_rule("""target goblin:\n add status \"dodge\" to goblin"""))


# print("\n\n\nRule: ")
# print("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 and then add status \"dodge\" to goblin""")
#print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp then reduce goblin.hp by 20"""))

# print(parser.is_valid_rule("""target point:\n if entity within (3, 3) of point and entity.hp < self.hp then reduce entity.hp to 6d6"""))
#print(parser.is_valid_condition("entity.hp += 6d6", "entity"))
# print(parser.get_regular_connectives("entity.hp += 6d6"))
# print("\n\n\nRule: ")
# print("target point:\n if entity within(3,3) of point then goblin.hp = 2")
# print(parser.is_valid_rule("""target point:\n if goblin within(3,3) of point then goblin.hp = 2"""))

# print("\n\n\nRule: ")
# print("target point:\n goblin.hp = 20\n if entity goblin (3, 3) of point and goblin.hp + 2 < self.spellsave then golbin.hp = 10")
# print(parser.is_valid_rule("""target point:\n goblin.hp = 20\n if goblin within(3, 3) of point and goblin.hp > 2 then goblin.hp = 10"""))


# print("\n\n\nRule: ")
# print("on goblin.Attack:\n Interrupt goblin.Attack if target has status “Dodge”:\n roll1 = d20\n roll2 = d20\n If roll1 < roll2 then roll1 = roll2\n If self.str + self.prof + roll1 > target.AC then decrease target.HP by 1d8 + self.str")
# print(parser.is_valid_rule("""on goblin.Attack:\n Interrupt goblin.Attack if target has status “Dodge”:\n roll1 = d20\n roll2 = d20\n If roll1 < roll2 then roll1 = roll2\n If self.str + self.prof + roll1 > target.AC then decrease target.HP by 1d8 + self.str\n """))

# print(parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll2 = roll2"))

# print(parser.is_valid_rule("interrupt goblin.Attack if target.statuses contains “Dodge”:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll1 = roll2"))