from syntax_parser import SyntaxParser

class _Validator(object):
    """
    Singleton Validator Class
    """

    def __init__(self):
        self._isValid = None
        self._allEntities = []
        self._syntaxParser = SyntaxParser()
    
    def is_valid_syntax(self, target, content):
        """
        Checks if the syntax of the content is valid

        Returns:
            if the content was valid syntax
        """
        return True
    
    def add_entity(self, entity):
        self._allEntities.append(entity)
    
    def remove_entity(self, entity):
        self._allEntities.remove(entity)
    
    def get_entities(self):
        return self._allEntities
    
    def set_entities(self, entities):
        self._allEntities = entities
    
    def parse_rule(self, content):
        _syntaxParser.parse_rule(content)
        return


_validator = _Validator()

def Validator(): return _validator

