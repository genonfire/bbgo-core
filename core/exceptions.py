from django.utils.log import AdminEmailHandler
from django.core import mail

from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

from core.wrapper import async_func
from utils.text import Text


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        if response.data.get('username'):
            error = response.data.get('username')[0]
            if error and error.code == 'unique':
                response.data = {
                    'username': [
                        ErrorDetail(Text.USERNAME_EXISTS, 'unique')
                    ]
                }

    return response


class ExceptionLogHandler(AdminEmailHandler):
    @async_func
    def send_mail(self, subject, message, *args, **kwargs):
        mail.mail_admins(
            subject, message, *args, connection=self.connection(), **kwargs
        )
