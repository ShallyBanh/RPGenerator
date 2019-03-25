from validator import Validator
from ruleset_parser_controller import RulesetParser

class ActionController:
    """
    Action Controller Class
    """

    def __init__(self):
        self._rulesetParser = RulesetParser()
    
    def perform_action(self, action):
        return