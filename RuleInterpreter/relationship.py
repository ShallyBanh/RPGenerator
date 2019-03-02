from action import Action
from entity import Entity


class Relationship:
    """
    Relationship Class
    """

    def __init__(self):
        self._entitiesInvolved = None
        self._actionsInvolved = None
        self._ruleContent = None
    
    def get_entities_involved(self):
        return self._entitiesInvolved

    def set_entities_involved(self, entities):
        self._entitiesInvolved = entities
    
    def add_entity(self, entity):
        self._entitiesInvolved.append(entity)
    
    def remove_entity(self, entity):
        self._entitiesInvolved.remove(entity)
    
    def get_actions_involved(self):
        return self._actionsInvolved

    def set_actions_involved(self, actions):
        self._actionsInvolved = actions
    
    def add_action_involved(self, action):
        self._actionsInvolved.append(action)
    
    def remove_action_involved(self, action):
        self._actionsInvolved.remove(action)

    def get_rule_content(self):
        return self._ruleContent

    def set_rule_content(self, content):
        self._ruleContent = content
    
    def execute_relationship(self):
        return 
    
    def __do_execute_relationship(self):
        return
