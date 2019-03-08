import re

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._conditionalIndicator = "__conditional_here__"

        self._keyWordsDict = { 
            ("=", "equal", "is", "are"): '==',
            ("reduce", "decrease", "subtract"): '-',
            ("increase", "add"): '+',
            ("multiply", "times", "time"): "*"
        }

        self._workingKeyWordsDict = {}
        for k, v in self._keyWordsDict.items():
            for key in k:
                self._workingKeyWordsDict[key] = v
    
    def generate_tab(self):
        """
        Generates a tab for a string

        Returns:
            a tab in string form
        """
        return "    "
    
    def generate_new_line(self):
        """
        Generates a new line and carriage return for a string.

        Returns:
            a new carriage return and a new line
        """
        return "\r\n"
    
    def get_if_statement_template(self):
        """
        Returns the if statement template for python

        Returns:
            if statement template for python as a string
        """
        return "if {}:".format(self._conditionalIndicator)

    def get_elif_statement_template(self):
        """
        Returns the elif statement template for python

        Returns:
            elif statement template for python as a string
        """
        return "elif {}:".format(self._conditionalIndicator)
    
    def get_else_statement_template(self):
        """
        Returns the else statement template for python

        Returns:
            else statement template for python as a string
        """
        return "else:"
    
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
    
    def is_target_rule(self, content):
        """
        Checks if the rule entered by the user is a target rule. I.e has the target keyword.
        returns true and a content else will return (false, false)

        Returns:
            Tuple - (isTargetRule, content inside the target rule)
        """
        firstCondition = content.find('{')

        if firstCondition != -1:
            condition = content[:firstCondition]
            targetIndex = condition.find("target")
            if targetIndex != -1:
                return(True, content[targetIndex + 6: firstCondition].strip())
                #here we should send it to the game enginer and wait and then pray it comes to the other parse_target function

        return (False, False)
    
    def is_rule_relationship(self):
        return 
    
    def parse_target(self, targetName, selectorEntity ,targetEntity, ruleSetContent):
        codeString = self.parse_code_from_rule(ruleSetContent)
        #replace self with selectorEntity 
        #replace target with target Entity
        codeString = codeString.replace(targetName, 'targetEntity') 
        codeString = codeString.replace('self', 'selectorEntity') 
        return codeString

    
    def parse_rule(self, content):
        """
        Parses the rule entered by the user into python friendly code as a string. 
        Will return a tuple containing if the rule is valid in the first cell and 
        the content if there is any in the second cell.

        Test cases:
        "target goblin{ if goblin.hp then subtract hp by 5" -> (False, False)
        "target goblin{ if goblin.hp then subtract hp by 5"} -> (True, 'if goblin.hp:\r\n    hp-= 5')

        Returns:
            tuple - (isValidRule, rule as python friendly string if exists)
        """
        content = content.lower()

        if content == False:
            return (False, False)
        if self.is_brackets_balanced(content) == False:
            return (False, False)
        if content.find("if") == -1 or content.find("then") == -1:
            return (False, False)

        isTarget, targetName = self.is_target_rule(content)
        if isTarget == False:
            return (False, False)

        print(self.parse_target(targetName, 1, 1, content))

        return (True, self.parse_code_from_rule(content))
    
    def parse_code_from_rule(self, content):
        """
        Parses the condition statement assumes that the user enter syntax is:
        if <condition>: <action>

        Returns:
            condition statement as python code string
        """
        content = self.parse_connectives(content)
        content = self.parse_keywords(content)

        return self.parse_conditionals_and_actions(content)   

    def parse_conditionals_and_actions(self, content):
        conditionalList = self.get_conditional_list(content)
        conditionsAndActionString = ""

        for conditionIndex in range(len(conditionalList)):
            if conditionalList[conditionIndex][0] == "if":
                conditional = self.parse_if_statement_conditional(content[conditionalList[conditionIndex][1] + 2: conditionalList[conditionIndex][2]].strip())

                if conditionIndex < len(conditionalList) - 1:
                    action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4: conditionalList[conditionIndex + 1][1]])
                else:
                    action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4:])

                conditionsAndActionString += conditional + action + self.generate_new_line()

            elif conditionalList[conditionIndex][0]  == "elif":
                conditional = self.parse_elif_statement_conditional(content[conditionalList[conditionIndex][1] + 7: conditionalList[conditionIndex][2]].strip())

                if conditionIndex < len(conditionalList) - 1:
                    action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4: conditionalList[conditionIndex + 1][1]])
                else:
                    action = self.parse_action(content[conditionalList[conditionIndex][2]+ 4:])

                conditionsAndActionString += conditional + action + self.generate_new_line()

            else:
                conditional = self.parse_else_statement_conditional()
                action = self.parse_action(content[conditionalList[conditionIndex][1]+ 4:])
                conditionsAndActionString += conditional + action.strip("}") + self.generate_new_line()

        return conditionsAndActionString
    
    def get_conditional_list(self, content):
        """
        Parses the condition statement assumes that the user enter syntax is:
        if <condition>: <action>

        Returns:
            condition statement as python code string
        """
        conditionalIndex = 0
        thenIndex = 0
        conditionalsList = []

        if content.find("if", conditionalIndex) != -1:
            conditionalIndex = content.find("if", conditionalIndex) + 1
            if content.find("then", thenIndex) != -1:
                thenIndex = content.find("then", thenIndex) + 1
                conditionalsList.append(("if", conditionalIndex, thenIndex))

        while content.find("if", conditionalIndex) != -1:
            conditionalIndex = content.find("if", conditionalIndex) + 1
            if content.find("then", thenIndex) != -1:
                thenIndex = content.find("then", thenIndex) + 1
                conditionalsList.append(("elif", conditionalIndex - 5, thenIndex))
            else:
                return
        
        if content.find("else", conditionalIndex) != -1:
            conditionalIndex = content.find("else", conditionalIndex) + 1
            if content.find("then", thenIndex) != -1:
                thenIndex = content.find("then", thenIndex) + 1
                conditionalsList.append(("else", conditionalIndex, thenIndex))
            else:
                conditionalsList.append(("else", conditionalIndex, len(content)))

        return conditionalsList
    

    def parse_else_statement_conditional(self):
        """
        Parses the condition statement assumes that the user enter syntax is:
        elif <condition>: <action>

        Returns:
            condition statement as python code string
        """
        return self.get_else_statement_template() + self.generate_new_line()

    def parse_elif_statement_conditional(self, content):
        """
        Parses the condition statement assumes that the user enter syntax is:
        elif <condition>: <action>

        Returns:
            condition statement as python code string
        """
        elif_statement = self.get_elif_statement_template().replace(self._conditionalIndicator, content) + self.generate_new_line()
        return elif_statement
    
    def parse_if_statement_conditional(self, content):
        """
        Parses the condition statement assumes that the user enter syntax is:
        if <condition>: <action>

        Returns:
            condition statement as python code string
        """
        if_statement = self.get_if_statement_template().replace(self._conditionalIndicator, content) + self.generate_new_line()
        return if_statement

    def parse_keywords(self, content):
        """
        Replaces key words from the user entered string to python syntax code

        Returns:
            string with key words replaced
        """
        for key, value in self._workingKeyWordsDict.items():
            content = content.replace(key, value)
        return content
    
    def parse_connectives(self, content):
        """
        Replaces natural language connectives from string as python connectives

        Returns:
            string with connectives replaced
        """
        content = content.replace("&", "and")
        content = content.replace("&&", "and")
        content = content.replace("||", "or")
        return content
    
    def parse_action(self, content):
        """
        Parses the actions statement assume that the user enter syntax is:
        if <condition>: <action>

        Returns:
            actions statement as python code string
        """
        actionStatement = self.generate_tab() + content.strip("}")

        #We are making the assuming that they user can use two types of connetors for actions
        # By and To
        # Ex. subtract hp by 5
        # ex. add 5 to hp
        byConnective = content.find('by')
        toConnective = content.find('to')

        if byConnective != -1:
            predicate = content[:byConnective].split()
            action = content[byConnective + 2:content.find('}')].strip()
            actionStatement = self.generate_tab() + predicate[1] + predicate[0] + "= " + action
        elif toConnective != -1:
            predicate = content[:toConnective].split()
            action = content[toConnective + 2:content.find('}')].strip()
            actionStatement = self.generate_tab() + action + predicate[0] + "= " + predicate[1]
        else:
            actionStatement = self.generate_tab() + content.strip()

        return actionStatement

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


a = SyntaxParser()
print(a.parse_rule("target goblin {else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str}"))
print(a.parse_rule("target goblin {if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else if (self.Str + self.Proficiency) + 1d20 > goblin.AC then reduce goblin.HP by 1d8 + self.Str else print()}"))
# print(a.parse_rule("target goblin{ if goblin.hp then subtract hp by 5"))
# print(a.parse_rule("target goblin{ if goblin.hp then INCREASE hp by 5}"))
# print(a.parse_rule("target goblin{ if self.hp then add 5 to hp}"))
# print(a.parse_rule("target goblin{ if 1 then print(\"testing\")}"))
# b = a.parse_rule("target goblin{ if 1 then print(\"testing\")}")
# print(b)
# # exec(b[1])
# print(a.is_target_rule("target goblin{ if goblin hp then act}"))
