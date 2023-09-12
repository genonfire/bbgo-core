from django.conf import settings

from accounts.tests import TestCase


class LoginTest(TestCase):
    def setUp(self):
        settings.USE_LOGIN_DEVICE = False

        self.create_user()

    def test_login_basic(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.status(200)
        self.check(self.data.get('key'), self.key)

    def test_login_check_wrong_username(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': '2@a.com',
                'password': self.password
            }
        )
        self.status(400)


class LoginUseDeviceTest(TestCase):
    def setUp(self):
        settings.USE_LOGIN_DEVICE = True

        self.create_user()

    def test_login_check_useragent(self):
        self.client = self.get_client('PC')
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.status(200)
        self.check(self.data.get('key'), self.key)

        login_device = self.data.get('login_device')
        self.check(login_device.get('device'), 'PC')
        self.check(login_device.get('os'), 'Mac OS X')
        self.check(login_device.get('browser'), 'Chrome')

    def test_login_check_wrong_password(self):
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': 'wrong_password'
            }
        )
        self.status(400)
