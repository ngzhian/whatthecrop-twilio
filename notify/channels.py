import logging

from django.conf import settings
from twilio.rest import TwilioRestClient

log = logging.getLogger(__name__)
 
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
my_number = "+12015966238"

def sms(to_number, message):
    """Uses Twilio to send a SMS to a phone number `to_number` with
    the sms content being `message`
    """
    client = TwilioRestClient(account_sid, auth_token)

    log.debug('event=sms to_number=%s, message=%s', to_number, message)

    client.messages.create(to=to_number, from_=my_number, body=message)
