import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

import twilio.twiml

from .models import FarmData, RawLog
from .parser import Parser
from .pusher import Pusher

log = logging.getLogger(__name__)

class RawLogList(ListView):
    model = RawLog

class FarmDataList(ListView):
    model = FarmData

@csrf_exempt
def handle_log(request):
    log.debug('event=handle_log data=%s', request.POST)

    phone_number = request.POST.get('From')
    message = request.POST.get('Body')
    state = request.POST.get('FromState')
    num_media = request.POST.get('NumMedia')
    if num_media:
        media_url = request.POST.get('MediaUrl0')
    else:
        media_url = None

    # check what kind of message this is
    # ideally we should have 2 separate endpoints for this 2 use case
    # but for demo this will be fine.
    if message and message.lower().startswith('bc:'):
        success = broadcast_message_to_state(state, message[3:])
        return make_twilio_response(success, 'Broadcasted')

    success = persist_farmer_message(phone_number, message, state, media_url)

    return make_twilio_response(success, 'Recorded')

def broadcast_message_to_state(state, message):
    from notify.views import broadcast
    response = broadcast(state, message)
    if response.status_code == 200:
        return True
    else:
        return False

def persist_farmer_message(phone_number, message, state, media_url):
    """In this method we want to do 3 things:
    1. record the raw message sent,
    2. record the parsed information
    3. push the parsed information to our servers to determine course of action
    """
    raw_log = record_raw_log(phone_number, message)
    if raw_log is None:
        # fail early, we failed to record the raw log due to validation errors
        return None

    farm_data = parse_and_record_clean_data(message, raw_log, state, media_url)
    push_data_to_intel(farm_data)
    return True

def make_twilio_response(success, message):
    """Make a http respones for the twilio callback"""
    resp = twilio.twiml.Response()
    if success:
        resp.message(message)
    else:
        resp.message('Failed, not ' + message.lower())
    return HttpResponse(str(resp))

def parse_and_record_clean_data(message, raw_log, state, media_url):
    parser = Parser()
    results = parser.parse(message)
    return record_clean_data(results, raw_log, state, media_url)

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

def record_clean_data(data, raw_log, state, media_url):
    log.debug('event=record_data data=%s', data)
    return FarmData.objects.create(
        crop=data['crop'],
        pest=data['pest'],
        harvest=data['harvest'],
        raw_log=raw_log,
        media_url = media_url,
        state=state or '',
    )

def push_data_to_intel(farm_data):
    Pusher.push(farm_data)
