import requests

from configurator import app_conf


class PushedAPIClient(object):

    API_URL = 'https://api.pushed.co/1/'

    @classmethod
    def push(cls, msg):
        """ Send push notifications
        https://about.pushed.co/docs/api#api-method-push
        """

        response = requests.post(cls.API_URL + 'push', data={
            'app_key': app_conf.pushed_app_key,
            'app_secret': app_conf.pushed_app_secret,
            'target_type': 'app',
            'content': msg,
        })

        print(response.text)
        print(msg)
