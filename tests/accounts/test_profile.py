from accounts.tests import TestCase


class ProfileTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_connect(self):
        self.post(
            '/api/accounts/connect/',
            auth=True
        )
        self.status(200)
        self.check(self.data.get('key'), self.key)
        self.check(self.data.get('user').get('username'), self.user.username)

    def test_get_profile(self):
        self.get(
            '/api/accounts/setting/',
            auth=True
        )
        self.status(200)
        self.check(self.data.get('username'), self.user.username)
        self.check(self.data.get('first_name'), self.user.first_name)
        self.check(self.data.get('last_name'), self.user.last_name)
        self.check(self.data.get('call_name'), self.user.call_name)
        self.check(self.data.get('is_approved'), self.user.is_approved)

    def test_update_profile(self):
        self.patch(
            '/api/accounts/setting/',
            {
                'username': 'b-boy@b.com',
                'first_name': 'B',
                'last_name': 'Boy',
                'call_name': 'B-Boy',
                'photo': self.gif(),
                'tel': '+82-10-1234-5678',
                'address': '3245 146th PL SE',
                'is_approved': not self.user.is_approved,
            },
            format='multipart',
            auth=True
        )
        self.status(200)
        self.check(self.data.get('username'), self.user.username)
        self.check(self.data.get('first_name'), 'B')
        self.check(self.data.get('last_name'), 'Boy')
        self.check(self.data.get('call_name'), 'B-Boy')
        self.check(self.data.get('tel'), '+82-10-1234-5678')
        self.check(self.data.get('address'), '3245 146th PL SE')
        self.check(self.data.get('is_approved'), self.user.is_approved)

    def test_callname_not_allow_null(self):
        self.patch(
            '/api/accounts/setting/',
            {
                'first_name': 'B',
                'call_name': None,
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/accounts/setting/',
            {
                'last_name': 'B',
                'call_name': '',
            },
            auth=True
        )
        self.status(400)
