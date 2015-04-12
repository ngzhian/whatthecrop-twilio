import codecs
import json
import logging

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rawlog.models import RawLog

from .channels import sms

log = logging.getLogger(__name__)

def console(request):
    if request.method == 'GET':
        return render(request, 'notify/console.html')
    if request.method == 'POST':
        return notify(request)

@csrf_exempt
def notify(request):
    """Accepts a POST request and dispatches according to the parameters.

    If a `id` parameter is found, this is assumed to be a sms to a single
    number, and the phone number will be looked up by finding a `RawLog`
    with primary key equals to `id`.

    If a `state` parameter is found, this is assumed to be a regional
    broadcast to an entire state in the US, and we will lookup
    `RawLog` by their state and send an sms to all of them.

    In both cases, the message that will be sent is specified by the
    paremter `body`

    e.g. POST {'id': '1', 'body': 'single sms'}
    e.g. POST {'state': 'NY', 'body': 'regional sms'}
    """
    log.debug('event=notify data=%s', request.POST)
    if request.POST.get('id'):
        raw_log_id = request.POST.get('id')
        message = request.POST.get('body')
        state = request.POST.get('state')
    else:
        payload = json.loads(codecs.decode(request.body, 'utf-8'))
        raw_log_id  = payload.get('id')
        message = payload.get('body')
        state  = payload.get('state')

    if raw_log_id:
        return single(raw_log_id, message)
    elif state:
        return broadcast(state, message)
    else:
        return HttpResponseNotFound('Missing log id')

def single(raw_log_id, message):
    try:
        raw_log = RawLog.objects.get(pk=raw_log_id)
        sms(raw_log.phone_number, message)
    except RawLog.DoesNotExist:
        return HttpResponseNotFound('log %d not found' % raw_log_id)
    return HttpResponse('Single sms success')

def broadcast(state, message):
    raw_logs = RawLog.objects.filter(state=state)
    for raw_log in raw_logs:
        sms(raw_log.phone_number, message)
    return HttpResponse('Broadcast to %s success', state)
