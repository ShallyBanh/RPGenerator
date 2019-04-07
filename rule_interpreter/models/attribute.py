"""
In this file, the following requirements are covered:
REQ-3.1.3.1 Ruleset Syntax
REQ-3.1.3.3: Entity Creation
REQ-3.1.3.4: Relationship Creation
"""
import numbers
class Attribute:
    """
    Attribute Class
    """

    def __init__(self, attributeName, attributeValue):
        self._attributeName = attributeName.lower()
        if (isinstance(attributeValue, str)):
            attributeValue = attributeValue.strip()
            if attributeValue.lower() == "true":
                self._attributeValue = True
                self._attributeType = bool
            elif attributeValue.lower() == "false":
                self._attributeValue = False
                self._attributeType = bool
            else:
                try:
                    self._attributeValue = float(attributeValue)
                    self._attributeType = float
                except:
                    self._attributeValue = attributeValue
                    self._attributeType = str
        elif (isinstance(attributeValue, bool)):
            self._attributeValue = attributeValue
            self._attributeType = bool
        elif (isinstance(attributeValue, numbers.Real)):
            self._attributeValue = float(attributeValue)
            self._attributeType = float
 
    def get_attribute_name(self):
        return self._attributeName

    def set_attribute_name(self, name):
        self._attributeName = name

    def get_attribute_value(self):
        return self._attributeValue 
        
    def get_attribute_type(self):
        return self._attributeType

    def set_attribute_value(self, attributeValue):
        self._attributeValue = attributeValue

    def __str__(self):
        return "Name: {}, Value: {}\n".format(self.get_attribute_name(), self.get_attribute_value())