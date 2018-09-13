from n26 import api
from n26 import config


class N26Connector(object):

    def __init__(self, username, password, card_id):
        # TODO: make self.api private
        self.api = api.Api(config.Config(
            username=username,
            password=password,
            card_id=card_id,
        ))

    def get_transactions(self, limit=50):
        return self.api.get_transactions_limited(limit)
