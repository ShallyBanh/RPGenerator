"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
from action import Action
from entity import Entity


class Relationship:
    """
    Relationship Class
    """

    def __init__(self, name, ruleContent):
        self._ruleContent = ruleContent
        self._interruptLine = ruleContent.splitlines()[0]
        self._interruptBehaviour = "\n".join(ruleContent.splitlines()[1:])
        self._name = name

    def get_name(self):
        return self._name
        
    def set_name(self, name):
        self._name = name

    def get_rule_content(self):
        return self._ruleContent

    def set_rule_content(self, content):
        self._ruleContent = content
        self._interruptLine = self._ruleContent.splitlines()[0]
        self._interruptBehaviour = "\n".join(self._ruleContent.splitlines()[1:])

    def get_interrupt_line(self):
        return self._interruptLine
        
    def get_interrupt_condition(self):
        return " ".join(self._interruptLine.split()[3:]).strip(':')
        
    def get_action_and_entity_interrupted(self):
        entity_dot_actionname = self.get_interrupt_line().split()[1]
        return entity_dot_actionname.split('.')
        
    def get_interrupt_behaviour(self):
        return self._interruptBehaviour