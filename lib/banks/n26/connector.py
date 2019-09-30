from n26 import api
from n26 import config


class N26Connector(object):

    def __init__(self, username, password):
        self._api = api.Api(config.Config(
            username=username,
            password=password,
            login_data_store_path=f".n26_access_token-{username}",
        ))

    def get_transactions(self, limit=50):
        return self._api.get_transactions_limited(limit)

    def get_balance(self):
        return self._api.get_balance()['usableBalance']
