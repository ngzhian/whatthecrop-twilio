import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import twilio.twiml

from .models import FarmData, RawLog
from .parser import Parser
from .pusher import Pusher

log = logging.getLogger(__name__)

@csrf_exempt
def handle_log(request):
    log.debug('event=handle_log data=%s', request.POST)

    phone_number = request.POST.get('From')
    message = request.POST.get('Body')

    success = persist_farmer_message(phone_number, message)

    return make_twilio_response(success)

def persist_farmer_message(phone_number, message):
    raw_log = record_raw_log(phone_number, message)
    if raw_log:
        farm_data = parse_and_record_clean_data(message, raw_log)
        push_data_to_intel(farm_data)
        return True
    return None

def make_twilio_response(recorded):
    """Make a http respones for the twilio callback"""
    resp = twilio.twiml.Response()
    if recorded:
        resp.message('Recorded!')
    else:
        resp.message('Failed, not recorded!')
    return HttpResponse(str(resp))

def parse_and_record_clean_data(message, raw_log):
    parser = Parser()
    results = parser.parse(message)
    return record_clean_data(results, raw_log)

def record_raw_log(phone_number, message):
    """Records the sent text from a farmer"""
    if phone_number and message:
        raw_log = RawLog.objects.create(
            phone_number=phone_number,
            raw_text=message
        )
        return raw_log
    else:
        return None

def record_clean_data(data, raw_log):
    log.debug('event=record_data data=%s', data)
    return FarmData.objects.create(
        crop=data['crop'],
        pest=data['pest'],
        harvest=data['harvest'],
        raw_log=raw_log,
    )

def push_data_to_intel(farm_data):
    Pusher.push(farm_data)
