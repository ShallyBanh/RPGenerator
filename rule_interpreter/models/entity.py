from action import Action
from size import Size

from validator import Validator 

class Entity:
    """
    Entity Class

    args:
        None for now
    """

    def __init__(self, name, entityType, width, height, isTemplate, inheritedFrom, x=0, y=0):
        self._type = entityType
        self._name = name
        self._image_filename = ""
        self._actions = [] 
        self._attributes = [] 
        self.size = Size(int(width),int(height)) 
        self._isTemplate = isTemplate
        self._currentStatuses = []
        self._isInheritedFrom = inheritedFrom
        self.x = x
        self.y = y
    

    def get_type(self):
        return self._type

    def set_type(self, typeToSet):
        self._type = typeToSet
    
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_image_filename(self):
        return self._image_filename

    def set_image_filename(self, id):
        self._image_filename = id

    def get_actions(self):
        return self._actions

    def set_actions(self, actions):
        self._actions = actions

    def get_attributes(self):
        return self._attributes

    def get_attributes_string(self):
        disp_str = ""
        for i in self.get_attributes():
            disp_str += str(i)
        return disp_str
		
    def get_attribute(self, attributeName):
        attributeName = attributeName.lower()
        for a in self._attributes:
            if a.get_attribute_name() == attributeName:
                return a
        print("No attribute of name " + attributeName + " found.")

    def set_attributes(self, attributes):
        self._attributes = attributes
    
    def add_attribute(self, attribute):
        if self.get_attributes == []:
            self._attributes.append(attribute)
            return 

        if attribute.get_attribute_name() in self.get_attributes():
            print("Error, attribute name already exists")
            return
        if attribute.get_attribute_name() == "location":
            print("error cannot name attribute location")
            return 

        self._attributes.append(attribute)
    
    def add_action(self, action):
        if self.get_actions() == []:
            self._actions.append(action)
            return 

        if action.get_action_name() in self.get_actions():
            print("Error, action name already exists")
            return
        # if action.get_action_name() == "location":
            # print("error cannot name action location")
            # return 

        self._actions.append(action)

    def get_size(self):
        return self.size

    def set_size(self, size):
        self.size = size

    def get_is_template(self):
        return self._isTemplate

    def set_is_template(self, isTemplate):
        self._isTemplate = isTemplate
    
    def get_is_inherited_from(self):
        return self._isInheritedFrom
    
    def get_current_statuses(self):
        return self._currentStatuses
    
    def set_current_statuses(self, currentStatuses):
        self._currentStatuses = currentStatuses

    def add_status(self, status):
        self._currentStatuses.append(status)
    
    def remove_status(self, status):
        self._currentStatuses.remove(status)
    
    def get_basic_entity_info_to_str(self):
        return "name: {}\ntype:{}\nwidth: {}\nheight: {}\nisTemplate: {}\ninheritedFrom: {}".format(self.get_name(), self.get_type(), self.get_size().get_width_as_string(), self.get_size().get_height_as_string(), self.get_is_template(), self.get_is_inherited_from())
            
    def __str__(self):
        return "Entity:\nName: {}\nwidth: {}\nheight: {}\ny: {}\nx: {}\nactions: {}\nattributes:\n{}".format(self.get_name(), self.get_size().get_width_as_string(), self.get_size().get_height_as_string(), str(self.x), str(self.y), str(self.get_actions()), self.get_attributes_string())


