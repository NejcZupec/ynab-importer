import json
import requests

from configurator import app_conf
from lib.log import logger


class PushedAPIClient(object):

    API_URL = 'https://api.pushed.co/1/'

    @classmethod
    def push(cls, msg):
        """ Send push notifications
        https://about.pushed.co/docs/api#api-method-push
        """

        logger.info('Pushing message via Pushed service...')

        response = requests.post(cls.API_URL + 'push', data={
            'app_key': app_conf.pushed_app_key,
            'app_secret': app_conf.pushed_app_secret,
            'target_type': 'app',
            'content': msg,
        })

        response_json = json.loads(response.text)

        if 'error' in response_json:
            msg = 'Message not sent. Error: {}'
            logger.error(msg.format(response_json['error']['message']))
            return

        response_type = response_json['response']['type']

        if response_type == 'shipment_successfully_sent':
            logger.info('Message successfully delivered to Pushed service')
        else:
            msg = 'Wrong response type from Pushed: {}'.format(response_type)
            logger.error(msg)
