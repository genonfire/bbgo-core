import datetime

from django.utils import timezone

from accounts.tests import TestCase


class SMSAuthTest(TestCase):
    def setUp(self):
        self.create_user(
            is_staff=True,
            is_approved=False,
        )

    def test_auth_sms_check_result(self):
        self.post(
            '/api/accounts/auth/sms/',
            {
                'tel': '1234-5678'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('tel'), '1234-5678')

    def test_auth_sms_check_permission(self):
        self.post(
            '/api/accounts/auth/sms/',
            {
                'tel': '010-1234-5678'
            }
        )
        self.status(401)

    def test_auth_sms_check_fields(self):
        self.post(
            '/api/accounts/auth/sms/',
            auth=True
        )
        self.status(400)

    def test_auth_sms_answer_correct_code(self):
        self.post(
            '/api/accounts/auth/sms/',
            {
                'tel': '010-1234-5678'
            },
            auth=True
        )

        pk = self.data.get('id')

        self.get(
            '/api/admin/auth_codes/%d/' % pk,
            auth=True
        )

        code = self.data.get('code')

        self.post(
            '/api/accounts/auth/%d/' % pk,
            {
                'code': code
            },
            auth=True
        )
        self.status(200)
        self.check_not(self.data.get('email'))
        self.check(self.data.get('tel'), '010-1234-5678')

        self.get(
            '/api/admin/auth_codes/%d/' % pk,
            auth=True
        )
        self.check(self.data.get('tel'), '010-1234-5678')
        self.check(self.data.get('code'), code)
        self.check(self.data.get('is_used'))

        self.get(
            '/api/accounts/setting/',
            auth=True
        )
        self.check(self.data.get('tel'), '010-1234-5678')
        self.check(self.data.get('is_approved'))

        self.post(
            '/api/accounts/auth/%d/' % pk,
            {
                'code': code
            },
            auth=True
        )
        self.status(400)

    def test_auth_sms_answer_wrong_code(self):
        auth_code = self.create_auth_code(tel='01012345678')

        self.get(
            '/api/admin/auth_codes/',
            auth=True
        )
        self.check_not(self.data[0].get('is_used'))
        self.check_not(self.data[0].get('tried_at'))
        self.check_not(self.data[0].get('wrong_input'))

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
                'code': str(int(auth_code.code) + 1)
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
                'code': auth_code.code
            },
            auth=True
        )
        self.status(400)

        self.get(
            '/api/accounts/setting/',
            auth=True
        )
        self.check_not(self.data.get('is_approved'))

        self.get(
            '/api/admin/auth_codes/?used=true&success=false&q=010',
            auth=True
        )
        for data in self.data:
            if data.get('id') == auth_code.id:
                self.check(data.get('is_used'))

    def test_auth_sms_answer_check_validation(self):
        then = timezone.localtime() - datetime.timedelta(days=1)
        auth_code = self.create_auth_code(
            tel='01011112222',
            created_at=then
        )

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
                'code': auth_code.code
            },
            auth=True
        )
        self.status(400)

        auth_code = self.create_auth_code(tel='01011112222')

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
                'code': auth_code.code
            },
        )
        self.status(401)

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
            },
            auth=True
        )
        self.status(400)
