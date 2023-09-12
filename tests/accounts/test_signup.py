from rest_framework.test import APIClient

from accounts.tests import TestCase


class SignupTest(TestCase):
    def setUp(self):
        self.client = APIClient(enforce_csrf_checks=True)
        self.username = 'bb@bbgo-test.com'
        self.password = 'password'
        self.first_name = 'B'
        self.last_name = 'B'

    def test_signup_check_duplicate_username(self):
        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        self.status(201)
        self.check(self.data.get('username'), self.username)
        self.check(self.data.get('first_name'), self.first_name)
        self.check(self.data.get('last_name'), self.last_name)
        self.check_in(
            self.data.get('call_name'),
            [
                '%s %s' % (self.first_name, self.last_name),
                '%s %s' % (self.last_name, self.first_name)
            ]
        )

        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        self.status(400)

    def test_signup_check_no_password(self):
        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name
            }
        )
        self.status(400)

    def test_signup_check_no_first_name(self):
        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'last_name': self.last_name
            }
        )
        self.status(400)

    def test_signup_check_no_last_name(self):
        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name
            }
        )
        self.status(400)

    def test_signup_check_null_fields(self):
        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': None,
                'last_name': self.last_name
            }
        )
        self.status(400)

        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': '',
                'last_name': self.last_name
            }
        )
        self.status(400)

        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': None
            }
        )
        self.status(400)

        self.post(
            '/api/accounts/signup/',
            {
                'username': self.username,
                'password': self.password,
                'first_name': self.first_name,
                'last_name': ''
            }
        )
        self.status(400)
