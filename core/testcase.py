import json
import accounts

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.response import Response as RestResponse
from rest_framework.test import APIClient, APITestCase

from core.response import Response


class TestCase(APITestCase):
    def log(self, *args, **kwargs):
        print("#", *args, **kwargs)

    def loooog(self, *args, **kwargs):
        log_func = getattr(self, 'log')
        log_func(*args, **kwargs)

    def response_log(self, response=None):
        if not response:
            response = self.response
        print(response, json.dumps(getattr(response, 'data', ''), indent=4))

    def status(self, *args, **kwargs):
        if isinstance(args[0], RestResponse):
            response = args[0]
            code_index = 1
        else:
            response = self.response
            code_index = 0

        if len(args[code_index:]) > 1:
            status_ok = False

            for arg in args[code_index:]:
                code = getattr(Response, 'HTTP_%d' % arg)

                if response.status_code == code:
                    status_ok = True
                    return

            if not status_ok:
                print(
                    '#',
                    args[code_index:],
                    response,
                    getattr(response, 'data', '')
                )
            assert status_ok
        else:
            code = getattr(Response, 'HTTP_%d' % args[code_index:])

            if response.status_code != code:
                print('#', code, response, getattr(response, 'data', ''))
            assert response.status_code == code

    def check(self, *args, **kwargs):
        if len(args) == 1:
            assert args[0]
        else:
            if args[0] != args[1]:
                self.loooog(kwargs.get('tag', ''), args[0], args[1])
            assert args[0] == args[1]

    def check_not(self, *args, **kwargs):
        if len(args) == 1:
            assert not args[0]
        else:
            if args[0] == args[1]:
                self.loooog(kwargs.get('tag', ''), args[0], args[1])
            assert args[0] != args[1]

    def check_in(self, *args, **kwargs):
        if args[0] not in args[1]:
            self.loooog(kwargs.get('tag', ''), args[0], args[1])
        assert args[0] in args[1]

    def check_gte(self, *args, **kwargs):
        if args[0] < args[1]:
            self.loooog(kwargs.get('tag', ''), args[0], args[1])
        assert args[0] >= args[1]

    def check_lte(self, *args, **kwargs):
        if args[0] > args[1]:
            self.loooog(kwargs.get('tag', ''), args[0], args[1])
        assert args[0] <= args[1]

    def check_between(self, *args, **kwargs):
        if args[0] < args[1]:
            self.loooog(kwargs.get('tag', ''), args[0], args[1])
        if args[0] > args[2]:
            self.loooog(kwargs.get('tag', ''), args[0], args[2])
        assert args[0] >= args[1] and args[0] <= args[2]

    def get(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.get(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.get(path, data, format=format, **extra)

        self.response = response
        if hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def post(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.post(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.post(path, data, format=format, **extra)

        self.response = response

        if response.status_code == Response.HTTP_400:
            self.error = response.data.get('error')
        elif hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def put(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.put(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.put(path, data, format=format, **extra)

        self.response = response
        if hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def patch(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.patch(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.patch(path, data, format=format, **extra)

        self.response = response
        if hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def delete(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.delete(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.delete(path, data, format, **extra)

        self.response = response
        if hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def options(self, path, data={}, format='json', auth=False, **extra):
        if auth:
            response = self.client.options(
                path, data, format=format,
                HTTP_AUTHORIZATION=self.auth_header, **extra
            )
        else:
            response = self.client.options(path, data, format, **extra)

        self.response = response
        if hasattr(response, 'data'):
            self.data = response.data.get('data')
        return response

    def get_client(self, device=None):
        if device == 'PC':
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'  # noqa
        else:
            user_agent = None

        return APIClient(enforce_csrf_checks=True, HTTP_USER_AGENT=user_agent)

    def file(
        self,
        name='test.txt',
        content=b'test',
        content_type='text/plain'
    ):
        return SimpleUploadedFile(name, content, content_type)

    def gif(
        self,
        name='image.gif',
    ):
        gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9'
            b'\x04\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02\x4c\x01\x00\x3b'
        )
        return SimpleUploadedFile(name, gif, 'image/gif')

    def png(
        self,
        name='image.png',
        content=b'data:image/png;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=',
        content_type='image/png'
    ):
        return SimpleUploadedFile(name, content, content_type)

    def create_user(
        self,
        username=None,
        first_name=accounts.tools.Test.FIRST_NAME,
        last_name=accounts.tools.Test.LAST_NAME,
        call_name=accounts.tools.Test.CALL_NAME,
        tel='010-1234-5678',
        address='Seoul',
        is_staff=False,
        is_superuser=False,
        is_approved=True,
        is_active=True,
    ):
        if not username:
            username = accounts.tools.Test.USERNAME

        self.username = username
        self.password = accounts.tools.Test.PASSWORD
        self.user = accounts.models.User.objects.create_user(
            username=self.username,
            email=self.username,
            password=self.password,
            first_name=first_name,
            last_name=last_name,
            call_name=call_name,
            tel=tel,
            address=address,
            is_approved=is_approved,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active
        )

        self.key = self.user.key()
        self.auth_header = 'Token ' + self.key
        return self.user
