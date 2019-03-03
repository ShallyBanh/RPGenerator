from validator import Validator

class Action:
    """
    Action Class
    """

    def __init__(self):
        self._actionName = None
        self._ruleContent = None
        self._validator = Validator()
    
    def get_action_name(self):
        return self._actionName

    def set_action_name(self, name):
        self._actionName = name
    
    def get_rule_content(self):
        return self._ruleContent 

    def set_rule_content(self, ruleContent):
        self._ruleContent = ruleContent

    def perform_action():
        return
    
    def __do_perform_action():
        return