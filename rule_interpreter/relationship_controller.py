from validator import Validator
from ruleset_parser_controller import RulesetParser

class RelationshipController:
    """
    Relationship Controller Class
    """

    def __init__(self):
        self._rulesetParser = RulesetParser()
    
    def evaluate_relationship(self, relationship):
        return