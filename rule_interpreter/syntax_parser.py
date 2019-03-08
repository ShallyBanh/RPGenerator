import re

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._conditionalIndicator = "__conditional_here__"

        self._keyWordsDict = { 
            ('=', 'equal','is', 'are'): '==',
            ('reduce', 'decrease', 'subtract'): '-',
            ('increase', 'add'): '+'
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

        return (False, False)
    
    def is_rule_relationship():
        return 
    
    def parse_target(self, selectorEntity ,targetEntity, ruleSetContent):
        return

    
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

        isRuleAction, target = self.is_target_rule(content)

        return (True, self.parse_code_from_rule(content))
    
    def parse_code_from_rule(self, content):
        """
        Parses the condition statement assumes that the user enter syntax is:
        if <condition>: <action>

        Returns:
            condition statement as python code string
        """
        ifIndex = content.find("if")
        thenIndex = content.find("then")

        content = self.parse_connectives(content)
        content = self.parse_keywords(content)
        conditional = self.parse_conditional(content[ifIndex + 2: thenIndex].strip())
        action = self.parse_action(content[thenIndex+ 5:])

        return conditional + action     
    
    def parse_conditional(self, content):
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
# print(a.parse_rule("target goblin{ if goblin.hp then subtract hp by 5}"))
# print(a.parse_rule("target goblin{ if goblin.hp then subtract hp by 5"))
# print(a.parse_rule("target goblin{ if goblin.hp then INCREASE hp by 5}"))
# print(a.parse_rule("target goblin{ if goblin.hp then add 5 to hp}"))
# print(a.parse_rule("target goblin{ if 1 then print(\"testing\")}"))
# b = a.parse_rule("target goblin{ if 1 then print(\"testing\")}")
# print(b)
# exec(b[1])
# print(a.is_target_rule("target goblin{ if goblin hp then act}"))
