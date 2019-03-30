import json
from .map import Map

class Game:
    def __init__(self):
        self.uniqueID = None
        self.GM = None
        self.name = None
        self.players = []
        self.map = None 
        self.ruleset_copy = None
        self.assets = []
        self.transcript = ""
    
    def __str__(self):
        string = "Game:"
        for k in self.__dict__.keys():
            string += "\n\t{}: {}".format(k, self.__dict__[k])
        return string

    def serialize(self):
        return self.__dict__

    def to_JSON(self):
        # automatically do nested calls https://stackoverflow.com/a/15538391
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,
                          indent=4)
    
    def get_uniqueID(self):
        return self.uniqueID

    def set_uniqueID(self, ID):
        self.uniqueID = ID

    def get_GM(self):
        return self.GM

    def set_GM(self, GM):
        self.GM = GM

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_players(self):
        return self.players

    def set_players(self, players):
        self.players = players

    def get_map(self):
        return self.map

    def set_map(self, map):
        self.map = map

    def get_ruleset_copy(self):
        return self.ruleset_copy

    def set_ruleset_copy(self, ruleset_copy):
        self.ruleset_copy = ruleset_copy

    def get_assets(self):
        return self.assets

    def add_asset(self, asset):
        self.assets.append(asset)

    def remove_asset(self, asset):
        self.assets.pop(asset.get_name, None)

    def get_transcript(self):
        return self.transcript

    def append_transcript(self, new_content):
        self.transcript += "\n" + new_content