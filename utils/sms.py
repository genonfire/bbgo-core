import json
import requests

from django.conf import settings

from utils.debug import Debug  # noqa
from utils.regexp import RegExpHelper


class _SMSHelper(object):
    ALIGO_RESULT_OK = '1'
    DIRECTSEND_RESULT_OK = '0'

    def send_sms_via_aligo(self, receiver, msg):
        if settings.DO_NOT_SEND_SMS:
            return

        data = {
            'key': settings.SMS_KEY,
            'user_id': settings.SMS_USER,
            'sender': settings.SMS_SENDER,
            'receiver': receiver,
            'msg': msg,
            # 'testmode_yn': 'Y'
        }

        Debug.trace(" Sending sms to %s" % receiver)

        response = requests.post(
            'https://apis.aligo.in/send/',
            data=data
        )

        results = json.loads(response.text)
        if results.get('result_code') != self.ALIGO_RESULT_OK:
            Debug.trace(
                " Error while sending sms to %s (%s)" % (
                    receiver,
                    results.get('message')
                )
            )

    def send_sms_via_directsend(self, recipients, msg):
        if settings.DO_NOT_SEND_SMS:
            return

        data = {
            'key': settings.SMS_KEY,
            'username': settings.SMS_USER,
            'sender': settings.SMS_SENDER,
            'recipients': recipients,
            'message': msg,
        }

        Debug.trace(" Sending sms to %s" % recipients)

        response = requests.post(
            'https://directsend.co.kr/index.php/api/v1',
            data=data
        )

        results = json.loads(response.text)
        if results.get('status') != self.DIRECTSEND_RESULT_OK:
            Debug.trace(
                " Error while sending sms to %s (%s)" % (
                    recipients,
                    results
                )
            )

    def recipients_serializer(self, recipients):
        if not isinstance(recipients, list):
            return recipients

        receiver = ''
        for index, recipient in enumerate(recipients):
            if index > 0:
                receiver += ','
            receiver += RegExpHelper.numbers(recipient)

        return receiver

    def send(self, recipients, msg):
        receiver = self.recipients_serializer(recipients)
        self.send_sms_via_aligo(receiver, msg)


SMSHelper = _SMSHelper()
