import json
import requests

from django.conf import settings

from core.wrapper import async_func
from utils.debug import Debug  # noqa


SLACK_URL_CHAT = 'https://slack.com/api/chat.postMessage'


class _SlackHelper(object):
    def get_headers(self):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer ' + settings.SLACK_TOKEN
        }
        return headers

    @async_func
    def chat(self, message):
        if not settings.SLACK_CHANNEL:
            return

        data = {
            'link_names': True,
            'channel': settings.SLACK_CHANNEL,
            'text': message
        }

        response = requests.post(
            SLACK_URL_CHAT,
            headers=self.get_headers(),
            data=json.dumps(data)
        )

        text = json.loads(response.text)
        if not text.get('ok'):
            Debug.trace(text)

    def shout(self, message):
        self.chat('@here ' + message)


SlackHelper = _SlackHelper()
