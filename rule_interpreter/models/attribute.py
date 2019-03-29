class Attribute:
    """
    Attribute Class
    """

    def __init__(self, attributeName, attributeValue):
        self._attributeName = attributeName.lower()
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
 
    def get_attribute_name(self):
        return self._attributeName

    def set_attribute_name(self, name):
        self._attributeName = name

    def get_attribute_value(self):
        return self._attributeValue 
        
    def get_attribute_type(self):
        return _self._attributeType

    def set_attribute_value(self, attributeValue):
        self._attributeValue = attributeValue

    def __str__(self):
        return "Name: {}, Value: {}\n".format(self.get_attribute_name(), self.get_attribute_value())