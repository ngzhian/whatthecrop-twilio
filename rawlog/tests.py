from unittest.mock import patch

from django.http import HttpRequest
from django.test import TestCase

from .models import FarmData, RawLog
from .views import handle_log
from .parser import Parser

@patch('rawlog.views.Pusher')
class HandleLogTestCase(TestCase):
    def test_endpoint_works(self, _):
        request = HttpRequest()
        request.path = '/l/'
        response = handle_log(request)
        self.assertIsNotNone(response)

    def test_raw_crop_data_fails_with_missing_data(self, _):
        request = HttpRequest()
        request.path = '/l/'
        request.POST['crop'] = 'A crop'
        response = handle_log(request)
        self.assertIn(b'Failed', response.content)

    def test_raw_crop_data_successfully_recorded(self, _):
        request = HttpRequest()
        request.path = '/l/'
        request.POST['crop'] = 'A crop'
        request.POST['From'] = 'a number'
        request.POST['Body'] = 'a message'
        response = handle_log(request)
        self.assertIn(b'Recorded', response.content)
        self.assertEqual(1, RawLog.objects.count())

    def test_crop_data_successfully_recorded(self, _):
        request = HttpRequest()
        request.path = '/l/'
        request.POST['crop'] = 'A crop'
        request.POST['From'] = 'a number'
        request.POST['Body'] = 'a message'
        response = handle_log(request)

        self.assertEqual(1, FarmData.objects.count())
        farm_data = FarmData.objects.first()
        self.assertEqual(farm_data.crop, 'a message')

    def test_crop_data_successfully_recorded_all_data_parsed_properly(self, _):
        request = HttpRequest()
        request.path = '/l/'
        request.POST['crop'] = 'A crop'
        request.POST['From'] = 'a number'
        request.POST['Body'] = 'a message'
        response = handle_log(request)

        self.assertEqual(1, FarmData.objects.count())
        farm_data = FarmData.objects.first()
        self.assertEqual(farm_data.crop, 'a message')

class ParserTestCase(TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse_crop(self):
        parsed = self.p.parse('a crop')
        self.assertEqual(parsed['crop'], 'a crop')

    def test_parse_crop_and_pest(self):
        parsed = self.p.parse('a crop, pest: a pest')
        self.assertEqual(parsed['crop'], 'a crop')
        self.assertEqual(parsed['pest'], 'a pest')

        parsed = self.p.parse('a crop, a pest')
        self.assertEqual(parsed['crop'], 'a crop')
        self.assertEqual(parsed['pest'], 'a pest')

    def test_parse_crop_pest_and_harvest(self):
        parsed = self.p.parse('a crop, pest: a pest, harvest')
        self.assertEqual(parsed['crop'], 'a crop')
        self.assertEqual(parsed['pest'], 'a pest')
        self.assertEqual(parsed['harvest'], 'harvest')

