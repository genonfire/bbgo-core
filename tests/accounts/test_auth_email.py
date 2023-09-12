import datetime

from django.utils import timezone

from accounts.tests import TestCase


class EmailAuthTest(TestCase):
    def setUp(self):
        self.create_user(
            is_staff=True,
            is_approved=False,
        )

    def test_auth_email_check_result(self):
        self.post(
            '/api/accounts/auth/email/',
            auth=True
        )
        self.status(201)
        self.check(self.data.get('email'), self.user.username)

    def test_auth_email_check_permission(self):
        self.post(
            '/api/accounts/auth/email/'
        )
        self.status(401)

    def test_auth_email_answer_correct_code(self):
        self.post(
            '/api/accounts/auth/email/',
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
        self.check(self.data.get('email'), self.user.username)
        self.check_not(self.data.get('tel'))

        self.get(
            '/api/accounts/setting/',
            auth=True
        )
        self.check(self.data.get('is_approved'))

        self.get(
            '/api/admin/auth_codes/%d/' % pk,
            auth=True
        )
        self.check(self.data.get('email'), self.user.username)
        self.check(self.data.get('code'), code)
        self.check(self.data.get('is_used'))

        self.post(
            '/api/accounts/auth/%d/' % pk,
            {
                'code': code
            },
            auth=True
        )
        self.status(400)

    def test_auth_email_answer_wrong_code(self):
        self.post(
            '/api/accounts/auth/email/',
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
                'code': str(int(code) + 1)
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
            '/api/admin/auth_codes/%d/' % pk,
            auth=True
        )
        self.check(self.data.get('email'), self.user.username)
        self.check(self.data.get('code'), code)
        self.check(self.data.get('is_used'))

        self.post(
            '/api/accounts/auth/%d/' % pk,
            {
                'code': code
            },
            auth=True
        )
        self.status(400)

    def test_auth_email_answer_check_validation(self):
        then = timezone.localtime() - datetime.timedelta(minutes=4)
        auth_code = self.create_auth_code(created_at=then)

        self.post(
            '/api/accounts/auth/%d/' % auth_code.id,
            {
                'code': auth_code.code
            },
            auth=True
        )
        self.status(400)

        auth_code = self.create_auth_code()

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
