from collections import namedtuple
import os

import yaml
import ynab

from lib.banks.n26.connector import N26Connector


CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'config.yml')


YNABAccount = namedtuple('YNABAccount', (
    'name',  # string
    'bank',  # string
    'connector',  # instance of Connector
    'ynab_account_id',  # string (UUID-like)
    'ynab_budget_id',  # string (UUID-like)
))


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
        self._configure_ynab_api()

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
                    bank=account['bank'],
                    connector=connector,
                    ynab_account_id=account['ynab_account_id'],
                    ynab_budget_id=account['ynab_budget_id'],
                ))

        except KeyError as e:
            field = e.args[0]
            msg = 'Field {} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg.format(field))

        return accounts

    @property
    def pushed_app_key(self):
        try:
            return self.cfg['pushed']['app_key']
        except KeyError as e:
            field = e.args[0]
            msg = 'Field {} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg.format(field))

    @property
    def pushed_app_secret(self):
        try:
            return self.cfg['pushed']['app_secret']
        except KeyError as e:
            field = e.args[0]
            msg = 'Field {} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg.format(field))

    def _configure_ynab_api(self):
        try:
            ynab_api_token = self.cfg['ynab']['api_token']
        except KeyError as e:
            field = e.args[0]
            msg = 'Field {} is missing. YNAB access token needed. See ' \
                  'config.yml.example file'
            raise ErrorInConfigFile(msg.format(field))
        configuration = ynab.Configuration()
        configuration.api_key['Authorization'] = ynab_api_token
        configuration.api_key_prefix['Authorization'] = 'Bearer'


app_conf = Configurator()
