class Ruleset:
    """
    Ruleset Class
    """

    def __init__(self):
        self._entities = None
        self._relationships = None
        self._importerExporter = None
    
    def get_entities(self):
        return self._entities

    def set_entities(self, entities):
        self._entities = entities
    
    def add_entities(self, entity):
        self._entities.append(entity)
    
    def remove_entities(self, entity):
        self._entities.remove(entity)

    def get_relationships(self):
        return self._relationships

    def set_relationships(self, relationships):
        self._relationships = relationships
    
    def add_relationship(self, relationship):
        self._relationships.append(relationship)

    def remove_relationship(self, relationship):
        self._relationships.remove(relationship)
    
    def get_rule_content(self):
        return self._ruleContent 

    def set_rule_content(self, ruleContent):
        self._ruleContent = ruleContent

    def export_ruleset():
        return

