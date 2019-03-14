from validator import Validator 
from entity import Entity
from syntax_parser import SyntaxParser
from attribute import Attribute
from action import Action
goblin = Entity("goblin", "steve", 1)
parser = SyntaxParser()

#print(parser.is_valid_rule("""target goblin:\n if 1 > 2 then 2"""))

# print("Rule: ")
# print("target goblin:\n if goblin.hp > 2 then 2")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then 2"""))

# print("\n\nAdding attribute: hp")
testAttribute = Attribute("hp", 1, 1)
goblin.add_attribute(testAttribute)
testAction = Action("Attack", 1)
goblin.set_actions([testAction])
print(goblin.get_actions())
goblin.add_status("Dodge")

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
# print(parser.is_valid_rule("""target goblin:\n add status \"dodge\" to goblin"""))


# print("\n\n\nRule: ")
# print("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 and then add status \"dodge\" to goblin""")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then add status \"dodge\" to goblin and goblin.hp = 20"""))


print("\n\n\nRule: ")
print("target point:\n if entity within(3,3) of point then goblin.hp = 2")
print(parser.is_valid_rule("""target point:\n if goblin within(3,3) of point then goblin.hp = 2"""))

print("\n\n\nRule: ")
print("target point:\n goblin.hp = 20\n if entity goblin (3, 3) of point and goblin.hp + 2 < self.spellsave then golbin.hp = 10")
print(parser.is_valid_rule("""target point:\n goblin.hp = 20\n if goblin within(3, 3) of point and goblin.hp > 2 then goblin.hp = 10"""))


# print("\n\n\nRule: ")
# print("on goblin.Attack:\n Interrupt goblin.Attack if target has status “Dodge”:\n roll1 = d20\n roll2 = d20\n If roll1 < roll2 then roll1 = roll2\n If self.str + self.prof + roll1 > target.AC then decrease target.HP by 1d8 + self.str")
# print(parser.is_valid_rule("""on goblin.Attack:\n Interrupt goblin.Attack if target has status “Dodge”:\n roll1 = d20\n roll2 = d20\n If roll1 < roll2 then roll1 = roll2\n If self.str + self.prof + roll1 > target.AC then decrease target.HP by 1d8 + self.str\n """))

print(parser.is_valid_rule("interrupt goblin.Attack if target.hp equals 5:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll2 = roll2"))

print(parser.is_valid_rule("interrupt goblin.Attack if target.statuses contains “Dodge”:\n roll1 = d20\n roll2 = d20\n if roll1 < roll2 then roll1 = roll2"))