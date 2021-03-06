"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
class Action:
    """
    Action Class
    """

    def __init__(self, name, content):
        if ' ' in name:
            raise Exception("Action name must not have spaces.")
        self._actionName = name.lower()
        self._ruleContent = content
        self._targetLine = self._ruleContent.splitlines()[0]
        self._actionBehaviour = "\n".join(self._ruleContent.splitlines()[1:])
    
    def get_action_name(self):
        return self._actionName

    def set_action_name(self, name):
        self._actionName = name
    
    def get_rule_content(self):
        return self._ruleContent

    def get_target_line(self):
        return self._targetLine

    def get_target_type(self):
        return self.get_target_line().strip().strip(':').split()[1]

    def get_action_behaviour(self):
        return self._actionBehaviour

    def set_rule_content(self, ruleContent):
        self._ruleContent = ruleContent
        self._targetLine = ruleContent.splitlines()[0]
        self._actionBehaviour = "\n".join(ruleContent.splitlines()[1:])
        
    def __str__(self):
        return "Name: {}\n".format(self.get_action_name())