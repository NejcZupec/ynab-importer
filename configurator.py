import os

import yaml


CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')


class ConfigFileNotFound(Exception):
    pass


class ErrorInConfigFile(Exception):
    pass


class Configurator(object):

    def __init__(self):
        try:
            self.cfg = yaml.safe_load(open(CONFIG_FILE_PATH, 'r'))
        except FileNotFoundError:
            msg = 'Copy config.yml.example to config.yml and configure all ' \
                  'relevant settings'
            raise ConfigFileNotFound(msg)

    @property
    def accounts(self):
        try:
            return self.cfg['accounts']
        except KeyError:
            msg = 'accounts are not defined. See config.yml.example file'
            raise ErrorInConfigFile(msg)


app_conf = Configurator()
