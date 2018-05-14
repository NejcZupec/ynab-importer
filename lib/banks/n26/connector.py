from n26 import api
from n26 import config

from lib.banks.n26.parser import TransactionsParser


class N26Connector(object):

    def __init__(self, username, password, card_id):
        self.api = api.Api(config.Config(
            username=username,
            password=password,
            card_id=card_id,
        ))

    def _get_transactions(self, limit=50):
        return self.api.get_transactions_limited(limit)

    def get_ynab_rows(self):
        transactions = self._get_transactions()
        parser = TransactionsParser(transactions)
        return parser.parse_rows()
