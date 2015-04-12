import requests

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
        requests.post(HADI_URL, data=payload)
