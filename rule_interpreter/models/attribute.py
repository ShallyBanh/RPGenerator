import numbers
class Attribute:
    """
    Attribute Class
    """

    def __init__(self, attributeName, attributeValue):
        self._attributeName = attributeName.lower()
        if isinstance(attributeValue, str):
            self._attributeType = "string"
        elif isinstance(attributeValue, bool):
            self._attributeType = "boolean"
        elif isinstance(attributeValue, numbers.Real):
            self._attributeType = "number"
        self._attributeValue = attributeValue
    
    def get_attribute_name(self):
        return self._attributeName

    def set_attribute_name(self, name):
        self._attributeName = name

    def get_attribute_value(self):
        return self._attributeValue 

    def set_attribute_value(self, attributeValue):
        self._attributeValue = attributeValue

    def __str__(self):
        return "Name: {}, Value: {}\n".format(self.get_attribute_name(), self.get_attribute_value())