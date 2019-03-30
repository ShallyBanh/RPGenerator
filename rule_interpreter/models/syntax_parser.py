import re
from validator import Validator

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._validConnectives = ["equals", "greater than", "less than", "greater or equal to", "less than or equal to", 
                                ">", ">=", "<", "<=", '+=', "-=" "not equal to", "not equal", "=", "==", "!=", "within", "has", "contains"]
        self._specialConnectives = ["by", "to", "towards", "away", "from"]
        self._actionCommands = ["move", "decrease", "increase", "reduce", "add", "multiply", "divide", "set"]
        self._arithmeticConnectives = ['*', '/', '+', '-']
        self._cannotFindSubstring = -1
        self._entityTarget = ""
        self._regexForDice = "[0-9]*d[0-9]+"
        self._variables_list = []
        self._validator = Validator()
    
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
        """
        Checks if the beginning of a rule entered by the user is a valid relationship rule.
        I.e "interrupt goblin.Attack if target.hp equals 5:"

        A relationship rule will always begin with "interrupt <action> if <condition>:"

        Returns:
            Tuple - (isValidBeginningOfRule, Action)
                - isValidBeginningOfRule: Bool - returns if the rule is valid
                - Action: String - The action we're interrupting i.e goblin.Attack
        """
        endOfRuleIndex = relationshipRuleLine.find(":")
        interruptIndex = relationshipRuleLine.find("interrupt")
        ifIndex = relationshipRuleLine.find("if")

        if endOfRuleIndex == self._cannotFindSubstring or interruptIndex == self._cannotFindSubstring or ifIndex == self._cannotFindSubstring:
            return (False, False)

        actionString = relationshipRuleLine[interruptIndex + len("interrupt"): ifIndex].strip()
        dotSplitter = actionString.find(".")
        if dotSplitter == self._cannotFindSubstring:
            return (False, False)

        target = actionString[:dotSplitter]
        if self.validate_object(actionString, target) == False:
            return (False, False)
        
        condition = relationshipRuleLine[ifIndex + 2:endOfRuleIndex]
        return (self.is_valid_condition(condition, "target"), actionString)

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
    
    def is_target_or_relationship_rule(self, content):
        """
        Checks if the rule entered is a valid target rule or a valid relationship rule.

        A relationship rule will always begin with "interrupt <action> if <condition>:"
        A target rule will always begin with "target <entity>:"

        Returns:
            Tuple - (isTargetOrRelationshipRule, TargetNameOrNameOfActionWeInterrupting)
                - isTargetOrRelationshipRule: Bool - returns if the rule is valid
                - TargetNameOrNameOfActionWeInterrupting: String - The action we're interrupting i.e goblin.Attack or the target name i.e goblin
        """
        endStatement = content.find("\n")
        colon = content.find(":")
        firstSpace = content.find(" ")
        if endStatement != self._cannotFindSubstring and colon != self._cannotFindSubstring:
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
        
        return (False, False)
        
    def is_valid_action_or_conditional_statement(self, content, targetName):
        """
        Checks if the content is a valid action statement or conditional statement.
        Examples of each statement:
            Action - "roll2 = 2"
            Conditional - "if goblin.hp > 2 then 2"

        Returns:
            Bool - True is the statement is valid and False otherwise
            
        """
        content = content.strip()

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

        thenIndex = content.find("then")

        # we should not have a then in the action statement
        if thenIndex != self._cannotFindSubstring:
            return False

        return self.is_valid_action(content, targetName)
    
    def is_valid_action(self, content, targetName):
        """
        Helper function to help validate the action statement assuming that the user enter syntax is:
        if <condition>: <action>
    
        Parameters:
            content: action statement without the then
            targetName: the name of the target

        Returns:
            if the action statement is valid
        """
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
            
            elif actionStatement[: actionStatement.find(" ")].strip() in self._actionCommands:
                if self.is_valid_special_action(actionStatement, targetName) == False:
                    return False
            
            elif actionStatement.find("to") == self._cannotFindSubstring and actionStatement.find("by") == self._cannotFindSubstring:
                if self.is_valid_condition(actionStatement, targetName) == False:
                    return False

        return True
    
    def is_valid_special_action(self, actionStatement, targetName):
        """
        Checks if the action statement is a valid special action command. Meaning instead of following the 
        generic <a> <connective> <b> we follow something of the form <actioncommand> <target> <byorto> <value>.
            Ex. Reduce goblin.hp by 2
            Ex. Reduce goblin.hp to 3
            Ex. Set x to 4
    
        Parameters:
            actionStatement: action statement
            targetName: the name of the target

        Returns:
            if the action statement is valid
        """
        actions = actionStatement.split(' ')
        actions = [x for x in actions if x]
        if len(actions) < 4:
            return False
        # the form will always be <action command> <targetname> <by or to> <number>
        if actions[0].strip() not in self._actionCommands:
            return False
        
        if actions[0].strip() == "move":
            if actions[2].strip().isdigit() == False:
                return False
    
            if actions[3].strip() not in self._specialConnectives:
                return False
            
            return self.validate_object(actions[1].strip(), targetName) and self.validate_object(actions[len(actions)-1].strip(), targetName)

        elif actions[0].strip() == "set":
            if actions[1].strip().isdigit() == True:
                return False
    
            if actions[2].strip() != "to":
                return False

            entityNames = [entity.get_name() for entity in self._validator.get_entities()]
            if actions[3].strip() not in self._variables_list and actions[3].strip() not in entityNames and actions[3].strip() != "target":
                self._variables_list.append(actions[3].strip())

            return self.validate_object(actions[3].strip(), targetName)
        
        else:
            if actions[2].strip() not in self._specialConnectives:
                return False
        
            return self.validate_object(actions[1].strip(), targetName) and self.validate_object(actions[3].strip(), targetName)
    
    def is_valid_status_action(self, content, targetName):
        """
        Helper function to help validate the action statement is a status action 
    
        Parameters:
            content: action statement without the then
            targetName: the name of the target

        Returns:
            if the action statement is valid
        """
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
            return False

        # if action is add then we should have to as the connector
        if action == "add":
            toIndex = content.find("to")
            if toIndex > targetIndex or toIndex < statusActionEndIndex:
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
        """
        validate any condition entered by the user assuming that the user enter syntax is:
        if <condition>: <action>
        ex. goblin.hp > 3

        Returns:
            if the condition is valid
        """
        #content: <a > b and c < d>
        # this is where the conditions will be located i,e >, <, => !=
        regularConnectiveIndicies = self.get_regular_connectives(content)
        andOrConnectiveIndicies = self.get_and_or_connectives(content)
        arithmeticConnectiveIndicies = self.get_arithmetic_connective(content)
        currentConnectiveIndex = 0
        if self.validate_connective_order(andOrConnectiveIndicies, regularConnectiveIndicies) == False:
            return False
        
        for i in range(len(regularConnectiveIndicies)):
            #special case with the within function
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
                
                if len(arithmeticConnectiveIndicies) != 0:
                    for arithmeticSymbol in self._arithmeticConnectives:
                        if rightHandSide.find(arithmeticSymbol) != self._cannotFindSubstring:
                            arithmeticSymbolSplitter = rightHandSide.find(arithmeticSymbol)
                            rhs = rightHandSide[:arithmeticSymbolSplitter].strip()
                            lhs = rightHandSide[arithmeticSymbolSplitter + 1:].strip()
                            # print("rhs")
                            # print(rhs)
                            # print("rhs validate")
                            # print(self.validate_object(rhs, target))
                            # print("lhs")
                            # print(lhs)
                            # print("lhs validate")
                            # print(self.validate_object(lhs, target))
                            if self.validate_object(leftHandSide, target) == False or self.validate_object(lhs, target) == False or self.validate_object(rhs, target) == False:
                                return False
                else:        
                    if self.validate_object(leftHandSide, target) == False or self.validate_object(rightHandSide, target, isStatus) == False:
                        # print("lhs validate. lhs is:")
                        # print(leftHandSide)
                        # print("lhs validate. result is:")
                        # print(self.validate_object(leftHandSide, target))
                        # print("rhs validate. rhs is:")
                        # print(rightHandSide)
                        # print("rhs validate. result is:")
                        # print(self.validate_object(rightHandSide, target))
                        return False
            
            if i < len(regularConnectiveIndicies) - 1: 
                currentConnectiveIndex = andOrConnectiveIndicies[i] + 3

        return True
    
    def is_valid_within_statement(self, connectiveIndex, content):
        """
        validate any condition that used the within statement (i.e mainly for our point target case)

        Returns:
            if the condition is valid
        """
        content = content.strip()
        allIndex = 0
        
        #all is valid
        if content[:3] == "all":
            allIndex = 4

        entity = content[allIndex:connectiveIndex - 1].strip()

        firstWithinBracket = content.find("(")
        endWithinBracket = content.find(")")
        self._entityTarget = entity
        if endWithinBracket < firstWithinBracket or firstWithinBracket < connectiveIndex:
            return False
        
        withinValues = content[firstWithinBracket +1:endWithinBracket]
        # then we only have 1 value
        if withinValues.find(",") == self._cannotFindSubstring:
            # not a number return false
            if not withinValues.isdigit():
                return False
        else:
            withinValuesList = withinValues.split(",")
            if len(withinValuesList) > 2 or not withinValuesList[0].strip().isdigit() or not withinValuesList[1].strip().isdigit():
                return False

        ofIndex = content.find("of")
        if ofIndex == self._cannotFindSubstring:
            return False 
        
        if entity == "point":
            entity = content[ofIndex + 3: ].strip()
            targetIndex = content.find(entity)
            self._entityTarget  = entity
        else:
            targetIndex = content.find("target")

        pointIndex = content.find("point")
        if pointIndex == self._cannotFindSubstring and targetIndex == self._cannotFindSubstring:
            return False

        if entity == "entity":
            return True

        for ob in self._validator.get_entities():
            if ob.get_type() == entity or ob.get_name() == entity:
                return True
        
        return False
    
    def validate_object(self, objectString, target, isStatus = False):
        """
        validates if the object entered by the user is a valid object, number, variable for our interpreter
        ex. goblin.hp
            - we validate the goblin exists and that hp exisit

        Returns:
            if the object is valid
        """
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
        if objectString.find(targetObject) != self._cannotFindSubstring and objectString.find(".") != self._cannotFindSubstring:
            dotSplitter = objectString.find(".")
            ourObject = objectString[:dotSplitter]
            objectAttribute = objectString[dotSplitter + 1:]
            if ourObject == "target" or ourObject == "entity" or ourObject == "self":
                return self.validate_generic_object_attribute(ourObject.strip(), objectAttribute.strip())
            else:
                return self.validate_object_attribute_or_action(ourObject.strip(), objectAttribute.strip())
        
        if objectString in self._variables_list:
            return True

        if objectString == "target" or objectString == "self" or objectString == "entity":
            return True

        return False
    
    def is_valid_status(self, target, status):
        """
        validates if the status entered by the user is a valid status. i.e the status exists

        Returns:
            if status entered is valid
        """
        #generic target so look through all entity statuses to find if we have a matching status
        if target == "target":
            for obj in self._validator.get_entities(): 
                for stat in obj.get_current_statuses():
                    stat = stat.lower()
                    if stat == status:
                        return True
        else:
            entity = None
            for ob in self._validator.get_entities():
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

        for ob in self._validator.get_entities():        
            #try to find the matching attribute
            for attribute in ob.get_attributes():
                if attribute.get_attribute_name() == attr:
                    return True
            
            #try to find the matching action
            for action in ob.get_actions():
                if action.get_action_name() == attr:
                    return True
        return False

    def validate_object_attribute_or_action(self, obj, attr):
        """
        validates if the object entered by the user is a valid object, number, variable for our interpreter
        ex. goblin.hp
            - we validate the goblin exists and that hp exists

        Returns:
            if the object is valid
        """
        entity = None
        for ob in self._validator.get_entities():
            if ob.get_type() == obj or ob.get_name() == obj:
                entity = ob
                break
        
        if entity is None:
            #no matching entity
            return False

        #try to find the matching attribute
        for attribute in entity.get_attributes():
            if str(attribute.get_attribute_name()) == str(attr):
                return True
        
        #try to find the matching action
        for action in entity.get_actions():
            if action.get_action_name() == attr:
                return True
        
        print("no matching attributes or actions")
        return False

    def validate_connective_order(self, andOrConnectives, regularConnectives):
        """
        validates that the order of connectives is valid. 
            - i.e "goblin.hp > 5 and target.hp > 5" ==> valid
            - i.e "goblin.hp > 5 target.hp > 5 and" ==> invalid

        Returns:
            if the connective order is valid
        """
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
        """
        Gets all the connectives from the content that is not "and" or "or"
            i.e >, < , =, equals, less than, etc 

        Returns:
            tuple(int, string) 
                - int -> the index of where the connective is found in the content
                - string -> the connective that we found
        """
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
                
                # there's an issue with "="" since if the connective is += it will match both += and = which is incorrect
                if len(connectiveIndicies) != 0 and connective == "=":
                    correctIndicies = connectiveIndicies
                    for c in connectiveIndicies:
                        symbolBeforeEqual = content[c[0]-1]
                        if symbolBeforeEqual == "+" or symbolBeforeEqual == "-" or symbolBeforeEqual == ">" or symbolBeforeEqual == "<":
                            correctIndicies.remove(c)
                    connectiveIndicies = correctIndicies

            currentConnectiveIndex = 0

        connectiveIndicies.sort()
        return connectiveIndicies

    def get_and_or_connectives(self, content):
        """
        Gets all the connectives from the content that is "and" or "or"
            i.e  and or or

        Returns:
            tuple(int, string) 
                - int -> the index of where the connective is found in the content
                - string -> the connective that we found
        """
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
    
    def get_arithmetic_connective(self, content):
        """
        Gets all arithmetic connectives:
            i.e +, -, *, /

        Returns:
            tuple(int, string) 
                - int -> the index of where the connective is found in the content
                - string -> the connective that we found
        """
        connectiveIndicies = []
        currentConnectiveIndex = 0

        for connective in self._arithmeticConnectives:
            if content.find(connective) != self._cannotFindSubstring:
                currentConnectiveIndex = content.find(connective, currentConnectiveIndex) + 1
                connectiveIndicies.append((currentConnectiveIndex -1, connective))
                while content.find(connective,currentConnectiveIndex) != -1:
                    currentConnectiveIndex = content.find(connective, currentConnectiveIndex) + 1
                    connectiveIndicies.append((currentConnectiveIndex -1, connective))
                
                # we need to check if the connective is += or just + since it will match to both + and += and if it is += we need to remove it
                if len(connectiveIndicies) != 0:
                    correctIndicies = connectiveIndicies
                    for c in connectiveIndicies:
                        symbolAfterConnective = content[c[0]+1]
                        if symbolAfterConnective == "=":
                            correctIndicies.remove(c)
                    connectiveIndicies = correctIndicies

            currentConnectiveIndex = 0

        connectiveIndicies.sort()
        return connectiveIndicies
            
    #the heart of the file
    def is_valid_rule(self, content, validator = Validator()):
        """
        Checks if a rule entered by the user is a valid rule. 

        Returns:
            Bool - true if the rule is true and false otherwise
        """
        self._validator = validator
        content = content.lower()
        colon = content.find(":")

        if self.is_brackets_balanced(content) == False:
            print("brackets not balanced")
            return False
        
        if self.is_target_or_relationship_rule(content)[0] == False:
            print("not a target or relationship")
            return False
        
        targetName = self.is_target_or_relationship_rule(content)[1]

        #empty targetname
        if len(targetName) == 0:
            return False

        return self.validate_action_conditional_rules_from_content(content[colon + 1:], targetName)

    def validate_action_conditional_rules_from_content(self, ruleContent, targetName):
        """
        Validates if all the actions and conditionals in the ruleContent is valid. 
        i.e
            target goblin:
                roll1 = d20
                if golbin.hp >4 then attack

        - it will validate this part:
            "roll1 = d20
            if golbin.hp >4 then attack"

        Returns:
            Bool - true if all the actions and conditionals in the rulecontent is true, false otherwise
        """
        actionOrConditionalList = ruleContent.strip().strip("}").split('\n')
        return self.validate_actions_or_conditionals_list(actionOrConditionalList, targetName)

    def validate_actions_or_conditionals_list(self, actionOrConditionalList, targetName):
        """
        Validates if the actions or conditionals in the actionOrConditionalList is valid. 
        i.e
            target goblin:
                roll1 = d20
                if golbin.hp >4 then attack

        - it will validate these statements individually [roll1 = d20, if golbin.hp >4 then attack]

        Returns:
            Bool - true if all the actions and conditionals in the actionOrConditionalList is true, false otherwise
        """
        for statement in actionOrConditionalList:
            if self.is_valid_action_or_conditional_statement(statement.strip(), targetName) == False:
                return False
        
        return True

