from map import Map

class GameEngine:
    """
    Game Engine Class
    args:
        None for now
    """

    def __init__(self):
        self._uniqueID = None
        self._name = None
        self._GM = None
        self._players = []
        self._entities = []
        self._map = None
        self._rulsetCopy = None
        self._assets = []

    def get_uniqueID(self):
        return self._uniqueID

    def set_uniqueID(self, uniqueID):
        self._uniqueID = uniqueID

    def get_GM(self):
        return _GM

    def set_GM(self, GM):
        self._GM = GM

    def get_name(self):
        return _name

    def set_name(self, name):
        self._name = name

    def get_players(self):
        return _players

    def set_players(self, players):
        self._players = players

    def get_entities(self):
        return _entities

    def set_entities(self, entities):
        self._entities = entities

    def get_map(self):
        return _map

    def set_map(self, map):
        self._map = map

    def get_rulesetCopy(self):
        return _rulesetCopy

    def set_rulesetCopy(self, rulesetCopy):
        self._rulesetCopy = rulesetCopy

    def get_assets(self):
        return _assets

    def add_asset(self, asset):
        self._assets.append(asset)

    def remove_asset(self, asset):
        self._assets.remove(asset)

