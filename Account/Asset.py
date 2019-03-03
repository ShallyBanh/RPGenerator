class Asset:
    def __init__(self, name):
        self._name = ""
        self._hashName = None # not
        self.file = "" # not
    
    def set_name(self, name):
        self._name = name
    
    def get_name(self):
        return self._name

    def generate_hashname(self, name):
        return
    
    def set_hashname(self, hashname):
        return