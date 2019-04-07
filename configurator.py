"""
This module contains the Configurator class that is utilized by server.py
"""

import configparser

class Configurator:
    """A configuration helper to abstract setup.

    Attributes:
        config_parser (configparser.ConfigParser) -- parser for config files.
        role (str) -- role/section of the owner.
        config (backports.configparser.SectionProxy) -- object representing the parsed configuration.

    """

    # @TODO database stuff

    def __init__(self, role="CLIENT", config_file = "config.conf"):
        """Initialize a Configurator

        Keyword arguments:
            role (str) -- role of owner (client/server).
        """

        self.config_parser = configparser.ConfigParser()
        self.role = role
        self.config_file = config_file
        self.config_parser.read(self.config_file)
        self.config = self.config_parser[self.role]

if __name__ == "__main__":
    configurator = Configurator()
    print(configurator.config_parser.sections())
    print(type(configurator.config))
