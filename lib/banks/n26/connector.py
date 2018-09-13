from n26 import api
from n26 import config


class N26Connector(object):

    def __init__(self, username, password, card_id):
        self._api = api.Api(config.Config(
            username=username,
            password=password,
            card_id=card_id,
        ))

    def get_transactions(self, limit=50):
        return self._api.get_transactions_limited(limit)

    def get_balance(self):
        return self._api.get_balance()['usableBalance']
