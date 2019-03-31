# RPGenerator

*Computer Software Enginnering Capstone Project*

Written by:

Bianca Angotti, Shally Banh, Andrew McKernan, Thomas Tetz


## Environment requirements
### macOS Install Instructions
macOS Mojave produces errors with Pygame. 

Known issue seen here: https://github.com/pygame/pygame/issues/555

**Requirement**: Download Python 3.7.2 from https://www.python.org for macOS 64-bit installer. 

### Windows Install Instructions
**Requirement**: Download Python 3.7.2 from https://www.python.org for Windows 10.

Note that the MAX_PATH limitation should be expanded (see https://docs.python.org/3/using/windows.html#installation-steps)

### pip3 Instructions
**For macOS**: 
`pip3 install --requirement requirements.txt --user`

Test pygame by running:
`python3 -m pygame.examples.aliens`


**For Windows Powershell**: 
`py -m pip install --requirement requirements.txt --user`

Test pygame by running:
`py -m pygame.examples.aliens`

### Docker Image Instructions
A Docker image exists for automated testing. It does not have graphical capability.

**Requirement**: Docker must be installed.

Pull the image:
```
docker pull ttetz/capstone-docker
```
Launch a container:
```
./docker_setup.sh -li
```

## RUNNING THE GAME

To run the game locally, spin up one instance of the server and one of the client game menu.

**Server:**
```
python3 server.py _keytoEncryptDatabase_
```
_keytoEncryptDatabase_ is the user's key to use to encrypt and decrypt their rulesets
**Client:**
```
python3 play_game.py
```

## WRITING RULES
Rules are written in Actions and in Relationships. They determine the actions that are able to be taken by Entities, and how they interact.
Every statement is ended by a new line. Indentation is ignored.

### Writing Actions:

Every Action starts off with a 'target' statement:
1. target self:
2. target {entity_type}:
3. target point:


After this statement, any usage of the word 'target' will be taken to refer to the targeted item.
1. You can target yourself (ie the acting entity). This makes any reference to 'target' refer to the acting entity. 
2. You can target a type of entity (ie select another entity of the given type from the map that you wish to affect). Any usages of the work 'target' will refer to the entity you have selected.
3. You can target a point on the map. Any usages of the word 'target' will refer to this chosen point.

### Writing Relationships:

Every Relationship starts off with an 'interrupt' statement:
1. interrupt {entity type}.{action name} if {condition}:
2. This statement means that when an action of name {action name} is performed by an entity of type {entity type}, then the action in question will no longer be performed. Instead, whatever statements follow the interrupt statement will be performed instead. The {condition} can include references to 'target' or 'self', which will refer to the 'self' or 'target' of the given action.


| Keyword | Explanation |
| ------- | ----------- |
|target|refers to the target of the given action|
|self|refers to the entity doing the action|
|{entity type}|an existing entity type. Used in the context of if [all] statements|

The following types of statements can be used to write a rule:


| Statement | Example | Explanation |
| --------- | ------- | ----------- |
| {number of dice}d{number of sides} |3d6 or d20|Randomly generates a number of values between 1 and {number of sides} {number of dice} times, and adds them all together. The {number of dice} is an optional requirement, and a d0 returns 0.|
| {entity}.{attribute} | goblin.HP | Get or set an entity's attribute. Used in other statements to view, check, and modify entity attributes as needed. |
| {variable or entity attribute} = {literal value}|x = 5, or y = "Sword"|A variable can be set to a real number, a string, or a boolean (True/False) value.|
| {variable name}|x|Get or set an existing variable. Used within a rule to store needed values.|
|increase {number, variable, or entity attribute} by {number} | increase target.hp by 10 | increase a given variable or entity attribute by the given number |
|decrease {number, variable, or entity attribute} by {number}| decrease target.hp by 6d6 | decrease a given variable or entity attribute by the given number|
|multiply {number, variable, or entity attribute} by {number}| multiply x by 10 | multiply a given variable or entity attribute by the given number|
|divide {number, variable, or entity attribute} by {number}| divide 100 by 4 | divide a given variable or entity attribute by the given number|
|set {variable or entity attribute} to {number, string, or boolean}| set target.hp to 100 | set a given variable or entity attribute by the given value|
|if [all] {condition} then {statement}|if target.ArmorClass < 5 then reduce target.hp by 10, or if all self within(2,2) of entity then reduce entity.hp by d4|if a given conditional statement is true, then execute the statement after the 'then'. The optional 'all' clause causes the statement to be evaluated for all entities of a given type present on the map. Make sure that you are using the 'all' clause if you wish to evaluate a conditional statement for all entities of a given type. The all clause will also evaluate the {statment} for every entity found that satisfies the {condition} statement.|
|{self, target, or entity type} within(x,y) of {self, target, or entity type}|self within(2,2) of target|checks if the given item is within a horizontal distance of (x) or a vertical distance of (y). Returns True or False for conditional statements. Ex. something at (2,2) is within(2,2) of something at (0,0).|
|move {entity} {number} away from {entity}|move target 3 away from self|Moves a given entity a number of tiles away from another entity. {entity} can be self, target, or an entity type in the case of an if all statement.|
|move {entity} {number} towards {entity}|move target 3 towards self|Moves a given entity a number of tiles towards another entity. {entity} can be self, target, or an entity type in the case of an if all statement.|
| {variable, number, or entity attribute} + {variable, number, or entity attribute}|x + 5, or target.hp + 8|Returns a value equal to the first value plus the second value. Used to assign something else to the sum of two values, such as self.hp = self.healAmount + 5|
| {variable, number, or entity attribute} - {variable, number, or entity attribute}|x - 5, or target.hp - 8|Returns a value equal to the first value minus the second value. Used to assign something else to the difference between two values, such as target.hp = target.hp - 5|
| {variable or entity attribute} = {variable, number, or entity attribute}|x = 5, or target.hp = 8, or target.|sets a given variable or entity attribute to the value given. |
| {variable, entity attribute, or number} == {variable, entity attribute, or number}|entity.hp == 5 or 5 == 8|Returns a true or false value (conditional) for whether the given values are equal. |
| {variable, entity attribute, or number} equals {variable, entity attribute, or number}|entity.hp equals 5 or 5 equals0 8|Returns a true or false value (conditional) for whether the given values are equal. |
| {variable, entity attribute, or number} < {variable, entity attribute, or number}|5 < 8 or entity.hp { 100|returns a true or false value whether the first number is less than the second number|
| {variable, entity attribute, or number} > {variable, entity attribute, or number}|5 > 8 or entity.hp } 100|returns a true or false value whether the first number is greater than the second number|
| {variable, entity attribute, or number} less than {variable, entity attribute, or number}|5 less than 8 or entity.hp less than 100|returns a true or false value whether the first number is less than the second number|
| {variable, entity attribute, or number} greater than {variable, entity attribute, or number}|5 greater than 8 or entity.hp greater than 100|returns a true or false value whether the first number is greater than the second number|
| {variable, entity attribute, or number} * {variable, entity attribute, or number}|5 * 4 or entity.hp * 6|Returns the result of the two given values multiplied together.|
| {variable, entity attribute, or number} / {variable, entity attribute, or number}| 16 / 4 or entity.hp/2|Returns the result of the first value divided by the second value.|
| {variable or entity attribute} += {variable, entity attribute, or number}| x += 4, or entity.hp += 5|Adds the given value to the variable or entity attribute and sets it to the result|
| {variable or entity attribute} -= {variable, entity attribute, or number}| x -= 4, or entity.hp -= 5|Subtracts the given value from the variable or entity attribute and sets it to the result|
| {variable or entity attribute} *= {variable, entity attribute, or number}| x *= 4, or entity.hp *= 5|Multiplies the given variable or entity attribute by the given factor and sets it to the result|
| {variable or entity attribute} /= {variable, entity attribute, or number}| x /= 4, or entity.hp /= 5|Divides the given variable or entity attribute by the given divisor and sets it to the result|
| {conditional} and {conditional}|4 { 1 and entity.hp } 10|If both {conditional} statements evaluate to True, returns true. Otherwise, returns False.|
| {conditional} or {conditional}|4 { 1 or entity.hp } 10|If one or both of the given {conditional} statements evaluates to True, returns True. Otherwise, returns False.|
| add status "{string}"to {target, self, or entity type}|add status "Dodge" to self, or add status "Poisoned" to target|Adds the status {string} to the entity, or entities in the case of an if all statement. |
| remove status "{string}" from {target, self, or entity type}|remove status "Poisoned" from self|Removes the status {string} from the entity, or entities in the case of an if all statement. |
| {target,self, or entity type}.statuses has "{string}"|self.statuses has "Poisoned"|Returns true or false as to whether the given status string is among the current statuses of the entity. |