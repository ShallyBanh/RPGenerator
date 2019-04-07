"""
In this file, the following requirements are covered:
REQ-3.2.3.10: Import visual assets
Note: This module contains the User class.
"""

class Asset:
    """An asset.

    Attributes:
        name(str) -- Asset's name.
        hashname(str) -- hash of the Asset's name.
        file (str) -- name of the file storing the Asset.

    """
    def __init__(self, name):
        """Initialize an Asset.

        Keyword arguments:
            name(str) -- Asset's name.
        """
        self._name = name
        self._hashname = None # not
        self._file = None # not

    def set_name(self, name):
        """Set the Asset's name."""
        self._name = name

    def get_name(self):
        """Get the Asset's name."""
        return self._name

    def generate_hashname(self):
        """Generate a hash based on the Asset's name."""
        return self._name + "hash"

    def set_hashname(self):
        """Set the Asset's hashname."""
        self._hashname = self.generate_hashname()
