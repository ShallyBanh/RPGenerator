from validator import Validator

class Action:
    """
    Action Class
    """

    def __init__(self, name, content):
        self._actionName = name
        self._ruleContent = content
        self._validator = Validator()
    
    def get_action_name(self):
        return self._actionName

    def set_action_name(self, name):
        self._actionName = name
    
    def get_rule_content(self):
        return self._ruleContent 

    def set_rule_content(self, ruleContent):
        self._ruleContent = ruleContent

    def perform_action(self):
        exec(self._ruleContent)
    
    def __do_perform_action(self):
        return
