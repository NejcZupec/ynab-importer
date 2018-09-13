import os

import yaml

from lib.banks.n26.connector import N26Connector
from lib.constants.ynab import YNABAccount


CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')


class ConfigFileNotFound(Exception):
    pass


class ErrorInConfigFile(Exception):
    pass


class BankConnectorNotImplemented(Exception):
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
        accounts = []

        try:
            for account in self.cfg['accounts']:
                if account['bank'] != 'n26':
                    msg = 'Bank {} is currently not supported. Contact ' \
                          'developers'.format(account['bank'])
                    raise BankConnectorNotImplemented(msg)

                connector = N26Connector(
                    username=account['settings']['username'],
                    password=account['settings']['password'],
                    card_id=account['settings']['card_id'],
                )

                accounts.append(YNABAccount(
                    name=account['name'],
                    connector=connector,
                ))

        except KeyError as e:
            field = e.args[0]
            msg = 'Field {} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg.format(field))

        return accounts


app_conf = Configurator()
