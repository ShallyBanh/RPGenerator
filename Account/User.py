# @TODO assets

class User:
    # @TODO database stuff
    def __init__(self, name, password, email):
        self._name = name
        self._password = password
        self._email = email
        self._assets = {}
    
    def set_name(self, name):
        self._name = name
    
    def get_name(self):
        return self._name

    def set_password(self, password):
        self._password = password
    
    def get_password(self):
        return self._password
    
    def set_email(self, email):
        self._email = email
    
    def get_email(self):
        return self._email

    def add_asset(self, asset):
        # @TODO any necessary checks, e.g. name conflict for same user
        # @TODO insert into database
        self._assets.append(asset)
    
    def update_asset(self, asset):
        return
    
    def delete_asset(self, asset):
        # @TODO delete from database
        self
    
    def get_asset(self, asset):
        return self._assets

    def set_assets(self, assetList):
        self._assets = assetList
    
    def get_assets(self):
        return self._assets