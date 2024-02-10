from django.utils.log import AdminEmailHandler
from django.core import mail

from rest_framework.views import exception_handler

from core.wrapper import async_func


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response and response.status_code == 400:
        if response.data and not response.data.get('error'):
            data = {
                'error': {
                    'code': 'DRF_FIELD_ERROR',
                    'message': '',
                    'field': response.data
                }
            }
            response.data = data

    return response


class ExceptionLogHandler(AdminEmailHandler):
    @async_func
    def send_mail(self, subject, message, *args, **kwargs):
        mail.mail_admins(
            subject, message, *args, connection=self.connection(), **kwargs
        )
