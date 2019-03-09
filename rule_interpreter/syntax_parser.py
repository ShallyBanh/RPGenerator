import re
from validator import Validator

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._validConnectives = ["equal", "greater than", "less than", "greater or equal to", "less than or equal to", 
                                ">", ">=", "<", "<=", "not equal to", "not equal", "=", "==", "!="]
        self._cannotFindSubstring = -1
    
    def is_brackets_balanced(self, expression):
        """
        Finds out if an expression is balanced 
        With a string containing only brackets.

        Test cases:
        is_brackets_balanced('[]()()(((([])))') -> False
        is_brackets_balanced('[](){{{[]}}}') -> True

        Returns:
            True if brackets are balanced
        """
        opening = tuple('({[')
        closing = tuple(')}]')
        mapping = dict(zip(opening, closing))
        queue = []

        for letter in expression:
            if letter in opening:
                queue.append(mapping[letter])
            elif letter in closing:
                if not queue or letter != queue.pop():
                    return False
        return not queue
    
    def is_valid_beginning_of_rule(self, targetOrRelationshipName, content):
        """
        Checks if the rule entered by the user is a target rule. I.e has the target keyword.
        returns true and a content else will return (false, false)

        Returns:
            Tuple - (isTargetRule, content inside the target rule)
        """
        firstCondition = content.find(':')
        if firstCondition != self._cannotFindSubstring :
            condition = content[:firstCondition]
            targetIndex = condition.find(targetOrRelationshipName)
            if targetIndex != self._cannotFindSubstring :
                #returning the target name
                return(True, content[targetIndex + 6: firstCondition].strip())
                #here we should send it to the game enginer and wait and then pray it comes to the other parse_target function

        return (False, False)
    
    def is_target_or_relationship(self, content):
        endStatement = content.find("\n")
        colon = content.find(":")
        if endStatement != self._cannotFindSubstring  and colon != self._cannotFindSubstring :
            if endStatement < colon:
                return (False, False)
            
            targetRule = self.is_valid_beginning_of_rule("target", content)
            if targetRule[0]:
                return targetRule
            
            relationshipRule = self.is_valid_beginning_of_rule("on", content)
            if relationshipRule[0]:
                return relationshipRule
        
        print("cannot find colon or new line")
        return (False, False)
    
    def is_rule_relationship(self):
        return 

    
    def validate_action_or_conditional_statement(self, content, targetName):
        endStatement = content.find("\n")

        if endStatement != self._cannotFindSubstring :
            fullStatement = content[:endStatement]
        else:
            fullStatement = content
        
        #we're a action statement
        # print("my if")
        # print(content[:2])
        if content[:2] == "if":
            # print("validate from if")
            return self.validate_if_statement_from_rule(content, targetName)
        else:
            # print("validate from action")
            return self.validate_action_statement_from_rule(content, targetName)
        
    def validate_action_statement_from_rule(self, content, targetName):
        """
        validate the action statement assumes that the user enter syntax is:
        if <condition>: <action>
    
        Parameters:
            content: action statement without the then
            targetName: the name of the target

        Returns:
            if the action statement is valid
        """
        # print("in validate action statement from rule")
        # print("content is:\n")
        # print(content)
        thenIndex = content.find("then")

        # we should not have a then in the action statement
        if thenIndex != self._cannotFindSubstring:
            return False
        
        return self.is_valid_action(content, targetName)
    
    def is_valid_action(self, content, targetName):
        # we can have multiple actions so we need to split 
        content = content.strip().strip("\n")
        
        #split actions by connector and since there is only and to connect actions
        actions = content.split("and")
        print("action statements")
        print(actions)
        for actionStatement in actions:
            # we are adding or removing statuses
            if actionStatement.find("status") != self._cannotFindSubstring:
                if self.is_valid_status_action(actionStatement, targetName) == False:
                    return False
            
            elif self.is_valid_condition(actionStatement, targetName) == False:
                return False

        return True
    
    def is_valid_status_action(self, content, targetName):
        statusIndex = content.find("status")
        statusActionBeginIndex = content.find('\"')

        if statusActionBeginIndex == self._cannotFindSubstring:
            return False

        if statusIndex == self._cannotFindSubstring:
            return False
        
        statusActionEndIndex = content.find('\"', statusActionBeginIndex)
        
        #check that status is always before the "actual status"
        if statusActionBeginIndex > statusActionEndIndex or statusActionBeginIndex < statusIndex:
            return False 
        
        #check that the beginning word is add or remove for status
        print("action for status")
        print(content[:statusIndex].strip())
        action = content[:statusIndex].strip()
        if action != "add" and action != "remove":
            return False

        #check that we're targeting our correct target to add statuses to 
        targetIndex = content.find(targetName) 
        print("action for target")
        print(content[targetIndex:].strip())
        if targetIndex == self._cannotFindSubstring:
            return False
        
        #check that target is at the end
        if content[targetIndex:].strip() != targetName:
            print("doesn't equal target name")
            return False

        # if action is add then we should have to as the connector
        if action == "add":
            print("in add statement")
            toIndex = content.find("to")
            if toIndex > targetIndex or toIndex < statusActionEndIndex:
                print("to index is wrong")
                return False
        
        # if action is add then we should have to as the connector
        if action == "remove":
            fromIndex = content.find("from")
            if fromIndex > fromIndex or fromIndex < statusActionEndIndex:
                return False 
        
        print("return true fro status")
        return True

    def validate_if_statement_from_rule(self, content, targetName):
        """
        validate the condition statement assumes that the user enter syntax is:
        if <condition>: <action>

        Returns:
            if the if statement is valid
        """
        thenIndex = content.find("then")

        if thenIndex == self._cannotFindSubstring:
            return False
        
        
        print(self.is_valid_condition(content[2:thenIndex], targetName))
        print("cehck is valid condition")
        return self.is_valid_condition(content[2:thenIndex], targetName) and self.is_valid_action(content[thenIndex + 4:], targetName)
    
    def is_valid_condition(self, content, target):
        #content: <a > b and c < d>
        # this is where the conditions will be located i,e >, <, => !=
        regularConnectiveIndicies = self.get_regular_connectives(content)
        andOrConnectiveIndicies = self.get_and_or_connectives(content)
        currentConnectiveIndex = 0
        # print("is in valid_condition")
        # print(content)
        if self.validate_connective_order(andOrConnectiveIndicies, regularConnectiveIndicies) == False:
            return False
        
        for i in range(len(regularConnectiveIndicies)):
            leftHandSide = content[currentConnectiveIndex: regularConnectiveIndicies[i]].strip()

            if i < len(andOrConnectiveIndicies):
                rightHandSide = content[regularConnectiveIndicies[i] + 1: andOrConnectiveIndicies[i]].strip()
            else:
                rightHandSide = content[regularConnectiveIndicies[i] + 1:].strip()

            if self.validate_object(leftHandSide, target) == False or self.validate_object(rightHandSide, target) == False:
                return False
            
            if i < len(regularConnectiveIndicies) - 1: 
                currentConnectiveIndex = andOrConnectiveIndicies[i] + 3
        
        return True
    
    def validate_object(self, objectString, target):
        # example 5 > 2
        if objectString.isdigit():
            return True
        
        # entity.hp > 4
        if objectString.find(target) != self._cannotFindSubstring:
            dotSplitter = objectString.find(".")
            ourObject = objectString[:dotSplitter]
            objectAttribute = objectString[dotSplitter + 1:]
            return self.validate_object_attribute(ourObject.strip(), objectAttribute.strip())

        return False
    
    def validate_object_attribute(self, obj, attr):
        entity = None
        for ob in Validator().get_entities():
            if ob.get_type() == obj or ob.get_name() == obj:
                entity = ob
                break
        
        if entity is None:
            #no matching entity
            return False
        
        #try to find the matching attribute
        for attribute in entity.get_attributes():
            if attribute.get_attribute_type() == attr or attribute.get_attribute_name() == attr:
                return True
        
        #try to find the matching action
        for action in entity.get_actions():
            if action.get_action_name() == attr:
                return True
        
        print("no matching attributes or actions")
        return False

    def validate_connective_order(self, andOrConnectives, regularConnectives):
        if len(regularConnectives) == 0:
            return False

        if len(andOrConnectives) >= len(regularConnectives):
            return False
        
        if len(andOrConnectives) != len(regularConnectives) - 1:
            return False
        
        #the logic here is that the the form would be 
        # a >b and c < v
        # so by this logic and and ors should be in between connectives
        for i in range(len(andOrConnectives)):
            if not (andOrConnectives[i] < regularConnectives[i +1] and andOrConnectives[i] > regularConnectives[i]):
                print("connectives are out of order")
                return False
        
        return True
    
    def get_regular_connectives(self, content):
        # this is where the conditions will be located i,e >, <, => !=
        connectiveIndicies = []
        findConnectives = True
        currentConnectiveIndex = 0
        oldConnectiveIndex = 0

        while findConnectives:
            oldConnectiveIndex = currentConnectiveIndex
            for connective in self._validConnectives:
                if content.find(connective, currentConnectiveIndex) != self._cannotFindSubstring:
                    # print("current")
                    # print(currentConnectiveIndex)
                    # print("connective to find")
                    # print(connective)
                    currentConnectiveIndex = content.find(connective, currentConnectiveIndex) + 1
                    connectiveIndicies.append(currentConnectiveIndex -1)
                    # print("after")
                    # print(currentConnectiveIndex)
                    # print("connective to find")
                    # print(connective)
                    continue
            if currentConnectiveIndex == oldConnectiveIndex:
                findConnectives = False

        return connectiveIndicies

    def get_and_or_connectives(self, content):
        andOrConnectivesIndicies = []
        currentConnectiveIndex = 0

        while content.find("and", currentConnectiveIndex) != self._cannotFindSubstring:
            currentConnectiveIndex = content.find("and", currentConnectiveIndex) + 1
            andOrConnectivesIndicies.append(currentConnectiveIndex - 1)
        
        currentConnectiveIndex = 0
        while content.find("or", currentConnectiveIndex) != self._cannotFindSubstring:
            currentConnectiveIndex = content.find("or", currentConnectiveIndex) + 1
            andOrConnectivesIndicies.append(currentConnectiveIndex - 1)

        andOrConnectivesIndicies.sort()
        return andOrConnectivesIndicies
    
    #the heart of the file
    def is_valid_rule(self, content):
        colon = content.find(":")

        if self.is_brackets_balanced(content) == False:
            print("brackets not balanced")
            return False
        
        if self.is_target_or_relationship(content)[0] == False:
            print("not a target or relationship")
            return False
        
        targetName = self.is_target_or_relationship(content)[1]

        #empty targetname
        if len(targetName) == 0:
            print("no target")
            return False

        if self.validate_action_or_conditional_statement(content[colon + 1:].strip().strip("}"), targetName) == False:
            print("not valid statement")
            return False
        
        return True


#### What is done so far
#   1.) we can parse a basic statement
#        ex. target goblin{ if goblin.hp then subtract hp by 5}
#   2.) two types of actions parsing are added i.e to and by 
#       ex. to -> add 5 to hp ====> hp+=5
#       ex. by -> subtract hp by 5 ====> hp-=5
#       ex. print("testing") =>  print("testing")
#   3.) Bracket checking to make sure that we have valid bracket closures
#   4.) Adding target as a keyword but so far only entities work    
#
#

## was working on parse target go and check and see if it works when you get home please. i.e create two entityes and run it and 
## see if it runs

### TODO
# 1.) make parser for point or be able to parse point
# 2.) make parser for relationships
# 3.) add more basic language to our dictionary
# 4.) Need to test with andrew to wait for user input and to see what we can do
#
#
#
#


# a = SyntaxParser()
# a.is_valid_rule("target goblin {else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str}")
# a.parse_rule("target goblin {if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else print()}")




# import re

# class SyntaxParser(object):
#     """
#     Syntax Parser Class
#     """

#     def __init__(self):
#         self._conditionalIndicator = "__conditional_here__"

#         self._keyWordsDict = { 
#             ("=", "equal", "is", "are"): '==',
#             ("reduce", "decrease", "subtract"): '-',
#             ("increase", "add"): '+',
#             ("multiply", "times", "time"): "*"
#         }

#         self._workingKeyWordsDict = {}
#         for k, v in self._keyWordsDict.items():
#             for key in k:
#                 self._workingKeyWordsDict[key] = v
    
#     def generate_tab(self):
#         """
#         Generates a tab for a string

#         Returns:
#             a tab in string form
#         """
#         return "    "
    
#     def generate_new_line(self):
#         """
#         Generates a new line and carriage return for a string.

#         Returns:
#             a new carriage return and a new line
#         """
#         return "\r\n"
    
#     def get_if_statement_template(self):
#         """
#         Returns the if statement template for python

#         Returns:
#             if statement template for python as a string
#         """
#         return "if {}:".format(self._conditionalIndicator)

#     def get_elif_statement_template(self):
#         """
#         Returns the elif statement template for python

#         Returns:
#             elif statement template for python as a string
#         """
#         return "elif {}:".format(self._conditionalIndicator)
    
#     def get_else_statement_template(self):
#         """
#         Returns the else statement template for python

#         Returns:
#             else statement template for python as a string
#         """
#         return "else:"
    
#     def is_brackets_balanced(self, expression):
#         """
#         Finds out if an expression is balanced 
#         With a string containing only brackets.

#         Test cases:
#         is_brackets_balanced('[]()()(((([])))') -> False
#         is_brackets_balanced('[](){{{[]}}}') -> True

#         Returns:
#             True if brackets are balanced
#         """
#         opening = tuple('({[')
#         closing = tuple(')}]')
#         mapping = dict(zip(opening, closing))
#         queue = []

#         for letter in expression:
#             if letter in opening:
#                 queue.append(mapping[letter])
#             elif letter in closing:
#                 if not queue or letter != queue.pop():
#                     return False
#         return not queue
    
#     def is_target_rule(self, content):
#         """
#         Checks if the rule entered by the user is a target rule. I.e has the target keyword.
#         returns true and a content else will return (false, false)

#         Returns:
#             Tuple - (isTargetRule, content inside the target rule)
#         """
#         firstCondition = content.find('{')

#         if firstCondition != -1:
#             condition = content[:firstCondition]
#             targetIndex = condition.find("target")
#             if targetIndex != -1:
#                 return(True, content[targetIndex + 6: firstCondition].strip())
#                 #here we should send it to the game enginer and wait and then pray it comes to the other parse_target function

#         return (False, False)
    
#     def is_rule_relationship(self):
#         return 
    
#     def parse_target_point(self, targetName, selectorEntity ,targetEntity, ruleSetContent, extraParams = []):

#         codeString = self.parse_code_from_rule(ruleSetContent)
#         codeString = codeString.replace(targetName, 'targetEntity') 
#         codeString = codeString.replace('point', 'selectorEntity.location')

#     def parse_target_entity(self, targetName, selectorEntity ,targetEntity, ruleSetContent, extraParams = []):
#         """
#         Parses the rule into python code. Note the game engine will call this to supply the 
#         entities to us

#         Returns:
#             string - python code represenation of the rule
#         """

#         codeString = self.parse_code_from_rule(ruleSetContent)
#         codeString = codeString.replace(targetName, 'targetEntity') 
#         codeString = codeString.replace('self', 'selectorEntity') 

#         return codeString

    
#     def parse_rule(self, content):
#         """
#         Parses the rule entered by the user into python friendly code as a string. 
#         Will return a tuple containing if the rule is valid in the first cell and 
#         the content if there is any in the second cell.

#         Test cases:
#         "target goblin{ if goblin.hp then subtract hp by 5" -> (False, False)
#         "target goblin{ if goblin.hp then subtract hp by 5"} -> (True, 'if goblin.hp:\r\n    hp-= 5')

#         Returns:
#             tuple - (isValidRule, rule as python friendly string if exists)
#         """
#         content = content.lower()

#         if content == False:
#             return (False, False)
#         if self.is_brackets_balanced(content) == False:
#             return (False, False)
#         if content.find("if") == -1 or content.find("then") == -1:
#             return (False, False)

#         isTarget, targetName = self.is_target_rule(content)
#         if isTarget == False:
#             return (False, False)

#         if targetName != "point":  
#             print(self.parse_target_entity(targetName, 1, 1, content))

#         return (True, self.parse_code_from_rule(content))
    
#     def parse_code_from_rule(self, content):
#         """
#         Parses the condition statement assumes that the user enter syntax is:
#         if <condition>: <action>

#         Returns:
#             condition statement as python code string
#         """
#         content = self.parse_connectives(content)
#         content = self.parse_keywords(content)

#         return self.parse_conditionals_and_actions(content)   

#     def parse_conditionals_and_actions(self, content):
#         conditionalList = self.get_conditional_list(content)
#         conditionsAndActionString = ""

#         for conditionIndex in range(len(conditionalList)):
#             if conditionalList[conditionIndex][0] == "if":
#                 conditional = self.parse_if_statement_conditional(content[conditionalList[conditionIndex][1] + 2: conditionalList[conditionIndex][2]].strip())

#                 if conditionIndex < len(conditionalList) - 1:
#                     action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4: conditionalList[conditionIndex + 1][1]])
#                 else:
#                     action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4:])

#                 conditionsAndActionString += conditional + action + self.generate_new_line()

#             elif conditionalList[conditionIndex][0]  == "elif":
#                 conditional = self.parse_elif_statement_conditional(content[conditionalList[conditionIndex][1] + 7: conditionalList[conditionIndex][2]].strip())

#                 if conditionIndex < len(conditionalList) - 1:
#                     action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4: conditionalList[conditionIndex + 1][1]])
#                 else:
#                     action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4:])

#                 conditionsAndActionString += conditional + action + self.generate_new_line()

#             else:
#                 conditional = self.parse_else_statement_conditional()
#                 action = self.parse_action(content[conditionalList[conditionIndex][1]+ 4:])
#                 conditionsAndActionString += conditional + action.strip("}") + self.generate_new_line()

#         return conditionsAndActionString
    
#     def get_conditional_list(self, content):
#         """
#         Parses the condition statement assumes that the user enter syntax is:
#         if <condition>: <action>

#         Returns:
#             condition statement as python code string
#         """
#         conditionalIndex = 0
#         thenIndex = 0
#         conditionalsList = []

#         if content.find("if", conditionalIndex) != -1:
#             conditionalIndex = content.find("if", conditionalIndex) + 1
#             if content.find("then", thenIndex) != -1:
#                 thenIndex = content.find("then", thenIndex) + 1
#                 conditionalsList.append(("if", conditionalIndex, thenIndex))

#         while content.find("if", conditionalIndex) != -1:
#             conditionalIndex = content.find("if", conditionalIndex) + 1
#             if content.find("then", thenIndex) != -1:
#                 thenIndex = content.find("then", thenIndex) + 1
#                 conditionalsList.append(("elif", conditionalIndex - 5, thenIndex))
#             else:
#                 return
        
#         if content.find("else", conditionalIndex) != -1:
#             conditionalIndex = content.find("else", conditionalIndex) + 1
#             if content.find("then", thenIndex) != -1:
#                 thenIndex = content.find("then", thenIndex) + 1
#                 conditionalsList.append(("else", conditionalIndex, thenIndex))
#             else:
#                 conditionalsList.append(("else", conditionalIndex, len(content)))

#         return conditionalsList
    

#     def parse_else_statement_conditional(self):
#         """
#         Parses the condition statement assumes that the user enter syntax is:
#         elif <condition>: <action>

#         Returns:
#             condition statement as python code string
#         """
#         return self.get_else_statement_template() + self.generate_new_line()

#     def parse_elif_statement_conditional(self, content):
#         """
#         Parses the condition statement assumes that the user enter syntax is:
#         elif <condition>: <action>

#         Returns:
#             condition statement as python code string
#         """
#         elif_statement = self.get_elif_statement_template().replace(self._conditionalIndicator, content) + self.generate_new_line()
#         return elif_statement
    
#     def parse_if_statement_conditional(self, content):
#         """
#         Parses the condition statement assumes that the user enter syntax is:
#         if <condition>: <action>

#         Returns:
#             condition statement as python code string
#         """
#         if_statement = self.get_if_statement_template().replace(self._conditionalIndicator, content) + self.generate_new_line()
#         return if_statement

#     def parse_keywords(self, content):
#         """
#         Replaces key words from the user entered string to python syntax code

#         Returns:
#             string with key words replaced
#         """
#         for key, value in self._workingKeyWordsDict.items():
#             content = content.replace(key, value)
#         return content
    
#     def parse_connectives(self, content):
#         """
#         Replaces natural language connectives from string as python connectives

#         Returns:
#             string with connectives replaced
#         """
#         content = content.replace("&", "and")
#         content = content.replace("&&", "and")
#         content = content.replace("||", "or")
#         return content
    
#     def parse_action(self, content):
#         """
#         Parses the actions statement assume that the user enter syntax is:
#         if <condition>: <action>

#         Returns:
#             actions statement as python code string
#         """
#         actionStatement = self.generate_tab() + content.strip("}")

#         #We are making the assuming that they user can use two types of connetors for actions
#         # By and To
#         # Ex. subtract hp by 5
#         # ex. add 5 to hp
#         byConnective = content.find('by')
#         toConnective = content.find('to')

#         if byConnective != -1:
#             predicate = content[:byConnective].split()
#             action = content[byConnective + 2:content.find('}')].strip()
#             actionStatement = self.generate_tab() + predicate[1] + predicate[0] + "= " + action
#         elif toConnective != -1:
#             predicate = content[:toConnective].split()
#             action = content[toConnective + 2:content.find('}')].strip()
#             actionStatement = self.generate_tab() + action + predicate[0] + "= " + predicate[1]
#         else:
#             actionStatement = self.generate_tab() + content.strip()

#         return actionStatement

# #### What is done so far
# #   1.) we can parse a basic statement
# #        ex. target goblin{ if goblin.hp then subtract hp by 5}
# #   2.) two types of actions parsing are added i.e to and by 
# #       ex. to -> add 5 to hp ====> hp+=5
# #       ex. by -> subtract hp by 5 ====> hp-=5
# #       ex. print("testing") =>  print("testing")
# #   3.) Bracket checking to make sure that we have valid bracket closures
# #   4.) Adding target as a keyword but so far only entities work    
# #
# #

# ## was working on parse target go and check and see if it works when you get home please. i.e create two entityes and run it and 
# ## see if it runs

# ### TODO
# # 1.) make parser for point or be able to parse point
# # 2.) make parser for relationships
# # 3.) add more basic language to our dictionary
# # 4.) Need to test with andrew to wait for user input and to see what we can do
# #
# #
# #
# #


# a = SyntaxParser()
# a.parse_rule("target goblin {else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str}")
# a.parse_rule("target goblin {if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else print()}")
# # print(a.parse_rule("target goblin{ if goblin.hp then subtract hp by 5"))
# # print(a.parse_rule("target goblin{ if goblin.hp then INCREASE hp by 5}"))
# # print(a.parse_rule("target goblin{ if self.hp then add 5 to hp}"))
# # print(a.parse_rule("target goblin{ if 1 then print(\"testing\")}"))
# # b = a.parse_rule("target goblin{ if 1 then print(\"testing\")}")
# # print(b)
# # # exec(b[1])
# # print(a.is_target_rule("target goblin{ if goblin hp then act}"))
