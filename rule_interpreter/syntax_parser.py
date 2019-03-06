import re

class SyntaxParser(object):
    """
    Syntax Parser Class
    """

    def __init__(self):
        self._conditionalIndicator = "__conditional_here__"

        self._keyWordsDict = { 
            ('=', 'equal','is', 'are'): '=='
        }

        self._workingKeyWordsDict = {}
        for k, v in self._keyWordsDict.items():
            for key in k:
                self._workingKeyWordsDict[key] = v
    
    def generate_tab(self):
        return "    "
    
    def get_if_statement_template(self):
        return "if {}:".format(self._conditionalIndicator)

    def get_elif_statement_template(self):
        return "elif {}:".format(self._conditionalIndicator)
    
    def get_else_statement_template(self):
        return "else:"
    
    def parse_rule(self, content):
        content = content.lower()
        ifIndex = content.find("if")
        #todo sanity checking
        thenIndex = content.find("then")
        #sanity checking 
        content = self.parse_conditional_from_connectives(content)
        content = self.parse_keywords(content)
        conditional = self.parse_conditional(content[ifIndex + 2: thenIndex].strip())
        action = self.parse_action(content[thenIndex+ 5:])
        return
    
    def parse_conditional(self, content):
        if_statement = self.get_if_statement_template().replace(self._conditionalIndicator, content)
        print(if_statement)
        return
    
    def parse_keywords(self, content):
        for key, value in self._workingKeyWordsDict.items():
            content = content.replace(key, value)
            print(key)
            print(content)
        return content
    
    def parse_conditional_from_connectives(self, content):
        content = content.replace("&", "and")
        content = content.replace("&&", "and")
        content = content.replace("||", "and")
        return content
    
    def parse_action(self, content):
        action_statement = self.generate_tab() + content
        print(action_statement)
        return


a = SyntaxParser()
a.parse_rule("if goblin hp is 1 then heal")
