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
		self._hierarchy = {}
    
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
		self._hierarchy[entity.get_type()] = []
		if entity.get_is_inherited_from() is not None:
			self._hierarchy[entity.get_is_inherited_from().get_type()].append(entity)
    
    def remove_entity(self, entity):
        if len(self._hierarchy[entity.get_type()]) < 1:
			self._allEntities.remove(entity)
			del self._hierarchy[entity.get_type()]
			if entity.get_is_inherited_from() is not None:
				self._hierarchy[entity.get_is_inherited_from().get_type()].remove(entity)
		else:
			pass
			#do not remove since it is a parent of other entities, which could break things.
			#TODO return an error code to determine whether the removal has succeeded.
			
		
    
    def get_entities(self):
        return self._allEntities
    
    def get_entity_idx(self, entityType):
        for entityIdx in range(len(self.get_entities())):
            if self.get_entities()[entityIdx].get_type() == entityType:
                return entityIdx
        
        return -1
    
    def update_attribute(self, entityIdx, oldAttributeIdx, attributeName, attributeValue):
        self._allEntities[entityIdx].update_attribute(oldAttributeIdx, Attribute(attributeName, attributeValue))
		for entity in self._hierarchy[self._allEntities[entityIdx].get_type()]:
			self._set_new_parent(entity, self._allEntities[entityIdx])

    def set_attribute(self, entityIdx, attributeName, attributeValue):
        self._allEntities[entityIdx].add_attribute(Attribute(attributeName, attributeValue))
		for entity in self._hierarchy[self._allEntities[entityIdx].get_type()]:
			self._set_new_parent(entity, self._allEntities[entityIdx])

    def update_action(self, entityIdx, oldActionIdx, actionName, ruleContent):
        self._allEntities[entityIdx].update_action(oldActionIdx, Action(actionName, ruleContent))
		for entity in self._hierarchy[self._allEntities[entityIdx].get_type()]:
			self._set_new_parent(entity, self._allEntities[entityIdx])
	
    def update_entity(self, entityIdx, newType, width, height, template, inheritedFrom):
		old_type = self._allEntities[entityIdx].get_type()
        self._allEntities[entityIdx].set_type(newType)
		self._hierarchy[newType] = self._hierarchy[old_type]
		del self._hierarchy[old_type]
        self._allEntities[entityIdx].set_size(Size(width, height))
        self._allEntities[entityIdx].set_is_template(template)
        self._allEntities[entityIdx].set_is_inherited_from(inheritedFrom)
		for entity in self._hierarchy[self._allEntities[entityIdx].get_type()]:
			self._set_new_parent(entity, self._allEntities[entityIdx])
		
	def _set_new_parent(self, child, parent):
		child.set_inherited_from(parent)
		for entity in self._hierarchy[child.get_type()]:
			self._set_new_parent(entity, child)

    def set_action(self, entityIdx, actionName, ruleContent):
        self._allEntities[entityIdx].add_action(Action(actionName, ruleContent))
		for entity in self._hierarchy[self._allEntities[entityIdx].get_type()]:
			self._set_new_parent(entity, self._allEntities[entityIdx])

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

