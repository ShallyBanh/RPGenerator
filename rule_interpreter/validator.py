from attribute import Attribute
from action import Action
class _Validator(object):
    """
    Singleton Validator Class
    """

    def __init__(self):
        self._isValid = None
        self._allEntities = []
    
    def is_valid_syntax(self, target, content):
        """
        Checks if the syntax of the content is valid

        Returns:
            if the content was valid syntax
        """
        return True
    
    def add_entity(self, entity):
        self._allEntities.append(entity)
    
    def remove_entity(self, entity):
        self._allEntities.remove(entity)
    
    def get_entities(self):
        return self._allEntities
    
    def get_entity_idx(self, name):
        for entityIdx in range(len(self.get_entities())):
            if self.get_entities()[entityIdx].get_name() == name:
                return entityIdx
        
        return -1
    
    def set_attribute(self, entityIdx, attributeName, attributeType, attributeValue):
        self._allEntities[entityIdx].add_attribute(Attribute(attributeName, attributeType, attributeValue))

    def set_action(self, entityIdx, actionName, ruleContent):
        self._allEntities[entityIdx].add_action(Action(actionName, ruleContent))

    def set_entity(self, idx, entity):
        self._allEntities[idx] = entity

    def set_entities(self, entities):
        self._allEntities = entities
    
    def clear_entities(self):
        self._allEntities = []
    
    def parse_rule(self, content):
        return


_validator = _Validator()

def Validator(): return _validator

