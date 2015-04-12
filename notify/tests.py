from unittest.mock import patch

from django.http import HttpRequest
from django.test import TestCase

from rawlog.models import RawLog

from .views import notify

STATE = 'NY'
BODY = 'body'
PHONE_NUMBER = '123'


class HandleLogTestCase(TestCase):
    def test_endpoint_works(self):
        request = HttpRequest()
        request.path = '/n/'
        response = notify(request)
        self.assertIsNotNone(response)

    @patch('notify.views.sms')
    def test_notify_single_message(self, mock_sms):
        raw_log = self.create_raw_log()
        response = self.client.post('/n/', {
            'id': raw_log.pk,
            'body': 'body',
        })
        mock_sms.assert_called_with('123', 'body')
        self.assertEqual(200, response.status_code)

    @patch('notify.views.sms')
    def test_notify_single_message(self, mock_sms):
        STATE = 'NY'
        BODY = 'body'
        raw_log = self.create_raw_log(state=STATE)
        response = self.client.post('/n/', {
            'state': STATE,
            'body': BODY,
        })
        mock_sms.assert_called_with('123', 'body')
        self.assertEqual(200, response.status_code)

    def create_raw_log(self, state=None):
        return RawLog.objects.create(
            phone_number=PHONE_NUMBER,
            state=STATE)
