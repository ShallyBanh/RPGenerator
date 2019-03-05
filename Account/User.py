"""This module contains the User class."""

class User:
    """A User account.

    Attributes:
        name (str) -- User's name.
        password (str) -- User's password.
        email (str) -- User's email.
        assets (dict) -- User's name. (default empty dict {})

    """

    # @TODO database stuff

    def __init__(self, name, password, email):
        """Initialize a User.

        Keyword arguments:
            name (str) -- User's name
            password (str) -- User's password
            email (str) -- User's email
        """
        self._name = name
        self._password = password
        self._email = email
        self._assets = {}

    def set_name(self, name):
        """Set the User's name."""
        self._name = name

    def get_name(self):
        """Get the User's name."""
        return self._name

    def set_password(self, password):
        """Set the User's password."""
        self._password = password

    def get_password(self):
        """Set the User's password."""
        return self._password

    def set_email(self, email):
        """Set the User's email."""
        self._email = email

    def get_email(self):
        """Set the User's email."""
        return self._email

    def add_asset(self, asset):
        """Add an asset to the User's asset dict."""
        # @TODO any necessary checks, e.g. name conflict for same user
        # @TODO insert into database
        self._assets.append(asset)

    def update_asset(self, asset):
        """Update one of the User's assets."""
        self._assets[asset.get_name] = asset

    def delete_asset(self, asset):
        """Delete one of the User's assets."""
        # @TODO delete from database
        self._assets.pop(asset.get_name, None)

    def get_asset(self, asset):
        """Return the specified asset of the User."""
        return self._assets[asset.get_name]

    def set_assets(self, asset_dict):
        """Set the User's dict of assets to the given dict."""
        self._assets = asset_dict

    def get_assets(self):
        """Get the User's dict of assets."""
        return self._assets
