from n26 import api
from n26.config import Config


class N26Connector(object):

    def __init__(self, username, password, device_token):
        self._username = username
        self._password = password
        self._device_token = device_token

    def _prepare_conf(self):
        conf = Config(validate=False)
        conf.USERNAME.value = self._username
        conf.PASSWORD.value = self._password
        conf.LOGIN_DATA_STORE_PATH.value = f"/tmp/.n26_access_token-{self._username}"
        conf.MFA_TYPE.value = "app"
        conf.DEVICE_TOKEN.value = self._device_token
        conf.validate()

        return conf

    def get_transactions(self, limit=50):
        n26_api = api.Api(self._prepare_conf())
        return n26_api.get_transactions_limited(limit)

    def get_balance(self):
        n26_api = api.Api(self._prepare_conf())
        return n26_api.get_balance()['usableBalance']
