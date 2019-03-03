from action import Action
from size import Size

class Entity:
    """
    Entity Class

    args:
        None for now
    """

    def __init__(self):
        self._type = None
        self._name = None
        self._id = None
        self._actions = None 
        self._attributes = None 
        self._size = None 
        self._isTemplate = None
        self._currentStatuses: None
    
    def get_type(self):
        return self._type

    def set_type(self, typeToSet):
        self._type = typeToSet
    
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_actions(self):
        return self._actions

    def set_actions(self, actions):
        self._actions = actions

    def get_attributes(self):
        return self._attributes

    def set_attributes(self, attributes):
        self._atrributes = atrributes

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size
    
    def get_is_template(self):
        return self._isTemplate

    def set_is_template(self, isTemplate):
        self._isTemplate = isTemplate
    
    def get_current_statuses(self):
        return self._currentStatuses
    
    def set_current_statuses(self, currentStatuses):
        self._currentStatuses = currentStatuses

    def add_status(self, status):
        self._currentStatuses.append(status)
    
    def remove_status(self, status):
        self._currentStatuses.remove(status)