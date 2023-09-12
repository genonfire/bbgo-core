from accounts.tests import TestCase
from utils.constants import Const


class UserDeactivateTest(TestCase):
    def setUp(self):
        self.person = self.create_user(
            username='jd@a.com',
            first_name='John',
            last_name='Doe',
            call_name='John Doe',
            tel='010-1234-5678',
            address='Seoul'
        )

    def test_check_censored_privacy(self):
        self.post(
            '/api/accounts/auth/sms/',
            {
                'tel': '010-1234-9876'
            },
            auth=True
        )
        self.post(
            '/api/accounts/deactivate/',
            {
                'consent': True,
            },
            auth=True
        )
        self.status(200)

        self.create_user(is_staff=True)
        self.get(
            '/api/admin/users/%d/' % self.person.id,
            auth=True
        )
        self.check_not(
            self.person.username.split('@')[0],
            self.data.get('username').split('@')[0]
        )
        self.check(
            self.data.get('username').split('@')[1],
            Const.CENSORED_EMAIL_DOMAIN.split('@')[1]
        )
        self.check(
            self.data.get('username')[0],
            self.person.username[0]
        )
        self.check_not(self.data.get('first_name'))
        self.check_not(self.data.get('last_name'))
        self.check_not(self.data.get('call_name'))
        self.check_not(self.data.get('tel'))
        self.check_not(self.data.get('address'))

        self.check_not(self.data.get('is_active'))

        self.get(
            '/api/admin/auth_codes/?q=010-1234-5678',
            auth=True
        )
        self.check(len(self.data), 0)

        self.get(
            '/api/admin/auth_codes/?q=jd@a.com',
            auth=True
        )
        self.check(len(self.data), 0)
