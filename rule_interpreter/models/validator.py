from attribute import Attribute
from action import Action
from size import Size
class _Validator(object):
    """
    Singleton Validator Class
    """

    def __init__(self):
        self._isValid = None
        self._allEntities = []
        self._allRelationships = []
    
    def is_valid_syntax(self, target, content):
        """
        Checks if the syntax of the content is valid

        Returns:
            if the content was valid syntax
        """
        return True
    
    def add_relationship(self, relationship):
        self._allRelationships.append(relationship)
    
    def remove_relationship(self, entity):
        self._allRelationships.remove(entity)
    
    def get_relationships(self):
        return self._allRelationships
    
    def get_relationship_idx(self, name):
        for relationshipIdx in range(len(self.get_relationships())):
            if self.get_relationships()[relationshipIdx].get_name() == name:
                return relationshipIdx
        
        return -1
    
    def add_entity(self, entity):
        self._allEntities.append(entity)
    
    def remove_entity(self, entity):
        self._allEntities.remove(entity)
    
    def get_entities(self):
        return self._allEntities
    
    def get_entity_idx(self, entityType):
        for entityIdx in range(len(self.get_entities())):
            if self.get_entities()[entityIdx].get_type() == entityType:
                return entityIdx
        
        return -1
    
    def update_attribute(self, entityIdx, oldAttributeIdx, attributeName, attributeValue):
        self._allEntities[entityIdx].update_attribute(oldAttributeIdx, Attribute(attributeName, attributeValue))

    def set_attribute(self, entityIdx, attributeName, attributeValue):
        self._allEntities[entityIdx].add_attribute(Attribute(attributeName, attributeValue))

    def update_action(self, entityIdx, oldActionIdx, actionName, ruleContent):
        self._allEntities[entityIdx].update_action(oldActionIdx, Action(actionName, ruleContent))
    
    def update_entity(self, entityIdx, newType, width, height, template, inheritedFrom):
        self._allEntities[entityIdx].set_type(newType)
        self._allEntities[entityIdx].set_size(Size(width, height))
        self._allEntities[entityIdx].set_is_template(template)
        self._allEntities[entityIdx].set_is_inherited_from(inheritedFrom)

    def set_action(self, entityIdx, actionName, ruleContent):
        self._allEntities[entityIdx].add_action(Action(actionName, ruleContent))

    def set_entity(self, idx, entity):
        self._allEntities[idx] = entity

    def set_entities(self, entities):
        self._allEntities = entities
    
    def set_relationships(self, relationships):
        self._allRelationships = relationships
    
    def clear_entities(self):
        self._allEntities = []
    
    def parse_rule(self, content):
        return


_validator = _Validator()

def Validator(): return _validator

