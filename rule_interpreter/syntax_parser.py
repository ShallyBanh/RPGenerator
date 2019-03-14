import re
from validator import Validator

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._validConnectives = ["equals", "greater than", "less than", "greater or equal to", "less than or equal to", 
                                ">", ">=", "<", "<=", "not equal to", "not equal", "=", "==", "!=", "within", "has", "contains"]
        self._otherConnectives = ["has", "have"]
        self._cannotFindSubstring = -1
        self._entityTarget = ""
        self._regexForDice = "[0-9]*d[0-9]+"
        self._variables_list = []
    
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
    
    def is_valid_beginning_of_relationship_rule(self, relationshipRuleLine):
        endOfRuleIndex = relationshipRuleLine.find(":")
        interruptIndex = relationshipRuleLine.find("interrupt")
        ifIndex = relationshipRuleLine.find("if")

        if endOfRuleIndex == self._cannotFindSubstring or interruptIndex == self._cannotFindSubstring or ifIndex == self._cannotFindSubstring:
            return False

        objectString = relationshipRuleLine[interruptIndex + len("interrupt"): ifIndex].strip()
        dotSplitter = objectString.find(".")
        if dotSplitter == self._cannotFindSubstring:
            return False

        target = objectString[:dotSplitter]
        if self.validate_object(objectString, target) == False:
            return False
        
        condition = relationshipRuleLine[ifIndex + 2:endOfRuleIndex]
        return (self.is_valid_condition(condition, "target"), objectString)


    def is_valid_beginning_of_target_rule(self, targetOrRelationshipName, content):
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
                return(True, content[targetIndex + len(targetOrRelationshipName): firstCondition].strip())

        return (False, False)
    
    def is_target_or_relationship(self, content):
        endStatement = content.find("\n")
        colon = content.find(":")
        firstSpace = content.find(" ")
        if endStatement != self._cannotFindSubstring and colon != self._cannotFindSubstring :
            if endStatement < colon:
                return (False, False)
            
            if content[:firstSpace] == "target":
                targetRule = self.is_valid_beginning_of_target_rule("target", content)
                if targetRule[0]:
                    return targetRule
            
            if content[:firstSpace] == "interrupt":
                relationshipRule = self.is_valid_beginning_of_relationship_rule(content)
                if relationshipRule[0]:
                    return relationshipRule
        
        print("cannot find colon or new line")
        return (False, False)
        
    def validate_action_or_conditional_statement(self, content, targetName):
        content = content.strip()
        #we're a action statement
        # print("my if")
        # print(content[:2])
        if content[:2] == "if":
            return self.validate_if_statement_from_rule(content, targetName)
        else:
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
        content = content.strip()
        
        #split actions by connector and since there is only and to connect actions
        # actions = re.split(r'(?:and )|[\n]+', content)
        actions = content.split('and')
        for actionStatement in actions:
            # we are adding or removing statuses
            actionStatement = actionStatement.strip()
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
        action = content[:statusIndex].strip()
        if action != "add" and action != "remove":
            return False

        #check that we're targeting our correct target to add statuses to 
        targetIndex = content.find(targetName) 
        if targetIndex == self._cannotFindSubstring:
            return False
        
        #check that target is at the end
        if content[targetIndex:].strip() != targetName:
            print("doesn't equal target name")
            return False

        # if action is add then we should have to as the connector
        if action == "add":
            toIndex = content.find("to")
            if toIndex > targetIndex or toIndex < statusActionEndIndex:
                print("to index is wrong")
                return False
        
        # if action is add then we should have to as the connector
        if action == "remove":
            fromIndex = content.find("from")
            if fromIndex > fromIndex or fromIndex < statusActionEndIndex:
                return False 
    
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
        
        return self.is_valid_condition(content[2:thenIndex], targetName) and self.is_valid_action(content[thenIndex + 4:], targetName)
    
    def is_valid_condition(self, content, target):
        #content: <a > b and c < d>
        # this is where the conditions will be located i,e >, <, => !=
        regularConnectiveIndicies = self.get_regular_connectives(content)
        andOrConnectiveIndicies = self.get_and_or_connectives(content)
        currentConnectiveIndex = 0
        if self.validate_connective_order(andOrConnectiveIndicies, regularConnectiveIndicies) == False:
            return False
        
        for i in range(len(regularConnectiveIndicies)):
            #special case with the within function
            # print("connective index")
            # print(andOrConnectiveIndicies)
            # print(regularConnectiveIndicies[i])
            if regularConnectiveIndicies[i][1] == "within":
                if self.is_valid_within_statement(regularConnectiveIndicies[i][0], content) == False:
                    return False 
            else:
                leftHandSide = content[currentConnectiveIndex: regularConnectiveIndicies[i][0]].strip()

                if i < len(andOrConnectiveIndicies):
                    rightHandSide = content[regularConnectiveIndicies[i][0] + 1: andOrConnectiveIndicies[i]].strip()
                else:
                    rightHandSide = content[regularConnectiveIndicies[i][0] + len(regularConnectiveIndicies[i][1]):].strip()

                # print("rhs")
                # print(rightHandSide)
                # print("lhs")
                # print(leftHandSide)
                # print(target)
                isStatus = (content.find("statuses") != -1)
                #we're doing an assignment so we have to add to our variable list
                if regularConnectiveIndicies[i][1] == "=":
                    if leftHandSide.isdigit() == False:
                        self._variables_list.append(leftHandSide)

                if self.validate_object(leftHandSide, target) == False or self.validate_object(rightHandSide, target, isStatus) == False:
                    # print("lhs validate")
                    # print(leftHandSide)
                    # print(self.validate_object(leftHandSide, target))
                    # print("rhs validate")
                    # print(rightHandSide)
                    # print(self.validate_object(rightHandSide, target))
                    return False
            
            if i < len(regularConnectiveIndicies) - 1: 
                currentConnectiveIndex = andOrConnectiveIndicies[i] + 3
        
        return True
    
    def is_valid_within_statement(self, connectiveIndex, content):
        content = content.strip()
        entity = content[:connectiveIndex - 1].strip()
        firstWithinBracket = content.find("(")
        endWithinBracket = content.find(")")
        self._entityTarget = entity
        if endWithinBracket < firstWithinBracket or firstWithinBracket < connectiveIndex:
            print("breakcets are off again")
            return False
        
        withinValues = content[firstWithinBracket +1:endWithinBracket]
        # then we only have 1 value
        if withinValues.find(",") == self._cannotFindSubstring:
            # not a number return false
            if not withinValues.isdigit():
                print("within values are not digit")
                return False
        
        withinValuesList = withinValues.split(",")
        if len(withinValuesList) > 2 or not withinValuesList[0].strip().isdigit() or not withinValuesList[1].strip().isdigit():
            print("indicies is wrong")
            return False
        
        pointIndex = content.find("point")
        if pointIndex == self._cannotFindSubstring:
            print("point is wrong")
            return False
        
        if content[endWithinBracket + 1: pointIndex].strip() != "of":
            print("of is wrong")
            return False
        
        for ob in Validator().get_entities():
            # print("my entity {}".format(entity))
            # print(ob.get_type())
            # print(ob.get_name())
            if ob.get_type() == entity or ob.get_name() == entity or entity == "entity":
                return True
        
        return False
    
    def validate_object(self, objectString, target, isStatus = False):
        # example 5 > 2
        targetObject = target 

        if objectString.isdigit():
            return True
        
        #list of valid terms other than digit i.e d20
        if re.search(self._regexForDice, objectString) is not None:
            return True

        #special case where the target is the point
        if target == "point":
            targetObject = self._entityTarget
        
        if isStatus != False:
            return self.is_valid_status(target, objectString)

        # entity.hp > 4
        if objectString.find(targetObject) != self._cannotFindSubstring:
            dotSplitter = objectString.find(".")
            ourObject = objectString[:dotSplitter]
            objectAttribute = objectString[dotSplitter + 1:]
            if ourObject == "target":
                return self.validate_generic_object_attribute(ourObject.strip(), objectAttribute.strip())
            else:
                return self.validate_object_attribute(ourObject.strip(), objectAttribute.strip())
        
        if objectString in self._variables_list:
            return True

        return False
    
    def is_valid_status(self, target, status):
        #generic target so look through all entity statuses to find if we have a matching status
        if target == "target":
            for obj in Validator().get_entities(): 
                for stat in obj.get_current_statuses():
                    stat = stat.lower()
                    if stat == status:
                        return True
        else:
            entity = None
            for ob in Validator().get_entities():
                if ob.get_type() == obj or ob.get_name() == obj:
                    entity = ob
                    break
            
            if entity is None:
                #no matching entity
                return False
            
            for stat in entity.get_current_statuses():
                stat = stat.lower()
                if stat == status:
                    return True

            return False
        
    
    def validate_generic_object_attribute(self, obj, attr):
        """
        This is method is used when the user has not specified a specific object but just a generic target object so
        we need search through everything that the entity has to find if the attribute or action or status exists
        """
        if attr == "statuses":
            return True

        for ob in Validator().get_entities():        
            #try to find the matching attribute
            for attribute in ob.get_attributes():
                if attribute.get_attribute_type() == attr or attribute.get_attribute_name() == attr:
                    return True
            
            #try to find the matching action
            for action in ob.get_actions():
                if action.get_action_name() == attr:
                    return True
        
        print("no matching attributes or actions")
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
            if not (andOrConnectives[i] < regularConnectives[i +1][0] and andOrConnectives[i] > regularConnectives[i][0]):
                print("connectives are out of order")
                return False
        
        return True
    
    def get_regular_connectives(self, content):
        # this is where the conditions will be located i,e >, <, => !=
        connectiveIndicies = []
        currentConnectiveIndex = 0

        for connective in self._validConnectives:
            if content.find(connective) != self._cannotFindSubstring:
                currentConnectiveIndex = content.find(connective, currentConnectiveIndex) + 1
                connectiveIndicies.append((currentConnectiveIndex -1, connective))
                while content.find(connective,currentConnectiveIndex) != -1:
                    currentConnectiveIndex = content.find(connective, currentConnectiveIndex) + 1
                    connectiveIndicies.append((currentConnectiveIndex -1, connective))
            currentConnectiveIndex = 0

        connectiveIndicies.sort()
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
    
    def is_valid_beginning_of_relationship_statement(self, content, target):
        dotIndex = content.find(".")
        onIndex = content.find("on")
        isValidEntity = False
        isValidAction = False
        # print("in releationship statement")
        if dotIndex == self._cannotFindSubstring:
            return False

        entity = content[onIndex + 3:dotIndex].strip()
        action = content[dotIndex + 1:]

        for obj in Validator().get_entities():
            if obj.get_type() == entity or obj.get_name() == entity:
                isValidEntity = True

            for objAction in obj.get_actions():
                if objAction.get_action_name() == action:
                    isValidAction = True
            
        if isValidAction == True and isValidEntity == True:
            print("valid relationship")
            return True
        
        return False
            

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
            return False

        return self.validate_action_conditional_rules_from_content(content[colon + 1:], targetName)

    def validate_action_conditional_rules_from_content(self, ruleContent, targetName):
            actionOrConditionalList = ruleContent.strip().strip("}").split('\n')
            return self.validate_actions_or_conditionals_list(actionOrConditionalList, targetName)

    def validate_actions_or_conditionals_list(self, actionOrConditionalList, targetName):
        for statement in actionOrConditionalList:
            if self.validate_action_or_conditional_statement(statement.strip(), targetName) == False:
                return False
        
        return True

