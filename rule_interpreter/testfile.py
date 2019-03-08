from validator import Validator 
from entity import Entity
from syntax_parser import SyntaxParser
from attribute import Attribute
goblin = Entity("goblin", "steve", 1)
parser = SyntaxParser()

#print(parser.is_valid_rule("""target goblin:\n if 1 > 2 then 2"""))

# print("Rule: ")
# print("target goblin:\n if goblin.hp > 2 then 2")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > 2 then 2"""))

# print("\n\nAdding attribute: hp")
testAttribute = Attribute("hp", 1, 1)
goblin.add_attribute(testAttribute)

# print("Rule: ")
# print("target goblin:\n if goblin.hp > 2 then 2")
# print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp then 2"""))


print("\n\n\nRule: ")
print("target goblin:\n if goblin.hp > 2 and goblin.hp > 2 then 2")
print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp and goblin.hp > 2 then 2"""))

print("\n\n\nRule: ")
print("target goblin:\n if goblin.hp > 2 goblin.hp > 2 and then 2")
print(parser.is_valid_rule("""target goblin:\n if goblin.hp > goblin.hp goblin.hp > 2 and then 2"""))
