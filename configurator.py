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
                    msg = f'Bank {account["bank"]} is currently not supported. Contact ' \
                          'developers'
                    raise BankConnectorNotImplemented(msg)

                connector = N26Connector(
                    username=account['settings']['username'],
                    password=account['settings']['password'],
                    device_token=account['settings']['device_token'],
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
            msg = f'Field {field} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg)

        return accounts

    @property
    def pushed_app_key(self):
        try:
            return self.cfg['pushed']['app_key']
        except KeyError as e:
            field = e.args[0]
            msg = f'Field {field} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg)

    @property
    def pushed_app_secret(self):
        try:
            return self.cfg['pushed']['app_secret']
        except KeyError as e:
            field = e.args[0]
            msg = f'Field {field} is missing. See config.yml.example file'
            raise ErrorInConfigFile(msg)

    def _configure_ynab_api(self):
        try:
            ynab_api_token = self.cfg['ynab']['api_token']
        except KeyError as e:
            field = e.args[0]
            msg = f'Field {field} is missing. YNAB access token needed. See ' \
                  'config.yml.example file'
            raise ErrorInConfigFile(msg)
        configuration = ynab.Configuration()
        configuration.api_key['Authorization'] = ynab_api_token
        configuration.api_key_prefix['Authorization'] = 'Bearer'


app_conf = Configurator()
