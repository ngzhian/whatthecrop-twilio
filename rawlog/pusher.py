import logging

import requests


log = logging.getLogger(__name__)

HADI_URL = 'http://whatthecropisthis.mybluemix.net/wtc/'

class Pusher(object):
    @classmethod
    def push(self, farm_data):
        # format farm_data into something hadi wants
        payload = {
            'id': farm_data.raw_log.pk,
            'crop': farm_data.crop,
            'pest': farm_data.pest,
            'harvest': farm_data.harvest,
            'media_url': farm_data.media_url,
            'state': farm_data.state,
        }
        log.debug('event=pusher payload=%s', payload)
        response = requests.post(HADI_URL, data=payload)
        log.debug('event=pusher response=%s', response)
