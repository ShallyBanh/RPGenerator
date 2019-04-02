import copy
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
        self._self_actions = []
        self._inherited_actions = []        
        self._self_attributes = []
        self._inherited_attributes = []
        self._combined_attributes = []
        self.size = Size(int(width),int(height)) 
        self._isTemplate = isTemplate
        self._currentStatuses = []
        self._isInheritedFrom = inheritedFrom
        if inheritedFrom is not None:
            if inheritedFrom.get_is_template():
                self._inherited_actions = copy.deepcopy(self._isInheritedFrom.get_actions())
                self._inherited_attributes = copy.deepcopy(self._isInheritedFrom.get_attributes())
            else:
                raise Exception("Given parent entity is not a template entity.")
        self.x = x
        self.y = y
    

    def get_type(self):
        return self._type

    def set_type(self, typeToSet):
        self._type = typeToSet.lower()
    
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_image_filename(self):
        return self._image_filename

    def set_image_filename(self, id):
        self._image_filename = id

    def get_actions(self):
        return self._self_actions + self._inherited_actions
        
    def get_action_names(self):
        names = []
        for action in self._self_actions + self._inherited_actions:
            names.append(action.get_action_name())
        return names

    def get_actions_string(self):
        return ", ".join(self.get_action_names())

    def set_actions(self, actions):
        self._self_actions = actions
        
    def add_action(self, action):
        self._self_actions.append(action)
        
    def update_action(self, oldIdx, action):
        self._self_actions[oldIdx].set_action_name(action.get_action_name())
        self._self_actions[oldIdx].set_rule_content(action.get_rule_content())

    def get_attributes(self):
        self._combined_attributes = self._self_attributes + self._inherited_attributes
        return self._combined_attributes

    def update_attribute(self, oldIdx, attribute):
        self._combined_attributes = self._self_attributes + self._inherited_attributes
        self._combined_attributes[oldIdx].set_attribute_name(attribute.get_attribute_name())
        self._combined_attributes[oldIdx].set_attribute_value(attribute.get_attribute_value())

    def get_attributes_string(self):
        disp_str = ""
        for i in self.get_attributes():
            disp_str += str(i)
        return disp_str
        
    def get_attribute(self, attributeName):
        attributeName = attributeName.lower()
        for a in self.get_attributes():
            if a.get_attribute_name() == attributeName:
                return a
        print("No attribute of name " + attributeName + " found.")

    # def set_attributes(self, attributes):
        # self._attributes = attributes
    
    def add_attribute(self, attribute):
        for a in self.get_attributes():
            if a.get_attribute_name() == attribute.get_attribute_name():
                raise Exception("An attribute with the name \"" + attribute.get_attribute_name() + "\" already exists.")

        self._self_attributes.append(attribute)
    
    def add_action(self, action):
        if self.get_actions() == []:
            self._self_actions.append(action)
            return 

        if action.get_action_name() in self.get_actions():
            print("Error, action name already exists")
            return

        self._self_actions.append(action)

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
        
    def set_inherited_from(self, parentEntity):
        if parentEntity.get_is_template():
            self._isInheritedFrom = parentEntity
            self._inherited_actions = copy.deepcopy(parentEntity.get_actions())
            self._inherited_attributes = copy.deepcopy(parentEntity.get_attributes())
        else:
            raise Exception("Given parent entity is not a template entity.")
            
    def is_of_type(self, type):
        isParentType = False
        if self._isInheritedFrom is not None:
            isParentType = self._isInheritedFrom.is_of_type(type)
        return type == self.get_type() or isParentType
    
    def set_is_inherited_from(self, isInheritance):
        self._isInheritedFrom = isInheritance
    
    def get_current_statuses(self):
        return self._currentStatuses
    
    def set_current_statuses(self, currentStatuses):
        self._currentStatuses = currentStatuses

    def add_status(self, status):
        self._currentStatuses.append(status)
    
    def remove_status(self, status):
        self._currentStatuses.remove(status)
    
    def get_basic_entity_info_to_str(self):
        return "name: {}\ntype:{}\nwidth: {}\nheight: {}\nisTemplate: {}\ninheritedFrom:\n\n {}".format(self.get_name(), self.get_type(), self.get_size().get_width_as_string(), self.get_size().get_height_as_string(), self.get_is_template(), self.get_is_inherited_from())
            
    def __str__(self):
        return "Entity:\nName: {}\nwidth: {}\nheight: {}\ny: {}\nx: {}\nactions: {}\nattributes:\n{}".format(self.get_name(), self.get_size().get_width_as_string(), self.get_size().get_height_as_string(), str(self.x), str(self.y), self.get_actions_string(), self.get_attributes_string())


