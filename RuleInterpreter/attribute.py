
class Attribute:
    """
    Attribute Class
    """

    def __init__(self):
        self._attributeName = None
        self._attributeType = None
        self._attributeValue = None
    
    def get_attribute_name(self):
        return self._attributeName

    def set_attribute_name(self, name):
        self._attributeName = name
    
    def get_attribute_type(self):
        return self._attributeType 

    def set_attribute_type(self, attributeType):
        self._attributeType = attributeType

    def get_attribute_value(self):
        return self._attributeValue 

    def set_attribute_value(self, attributeValue):
        self._attributeValue = attributeValue