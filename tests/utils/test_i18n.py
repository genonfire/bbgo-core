from core.testcase import TestCase
from utils.text import Text


class I18NTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_i18n_prefix(self):
        response = self.post(
            '/en/api/accounts/login/',
            {
                'username': '1@a.com',
                'password': 'passworD'
            }
        )
        self.status(response, 400)
        self.check(self.error.get('code'), 'UNABLE_TO_LOGIN')
        self.check(self.error.get('message'), 'Unable to login.')

    def test_i18n_default_no_prefix(self):
        response = self.post(
            '/api/accounts/login/',
            {
                'username': '1@a.com',
                'password': 'passworD'
            }
        )
        self.status(response, 400)
        self.check(self.error.get('code'), 'UNABLE_TO_LOGIN')
        self.check(self.error.get('message'), Text.UNABLE_TO_LOGIN)

    def test_i18n_error(self):
        response = self.post(
            '/api/accounts/login/',
            {
            }
        )
        self.status(response, 400)
        self.check(self.error.get('code'), 'DRF_FIELD_ERROR')
        self.check(self.error.get('keys'), ['username', 'password'])
        self.check(
            list(self.error.get('field').keys()),
            ['username', 'password']
        )
