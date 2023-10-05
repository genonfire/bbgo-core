from accounts.tests import TestCase
from utils.constants import Const


class UserAdminTest(TestCase):
    def setUp(self):
        self.user_a = self.create_user(username='a@a.com')
        self.user_b = self.create_user(username='b@a.com')
        self.staff = self.create_user(
            username='c@a.com',
            is_staff=True,
            is_superuser=True,
        )

    def test_user_admin_permission(self):
        self.patch(
            '/api/admin/users/%d/' % self.user_a.id,
            {
                'call_name': 'A'
            }
        )
        self.status(401)

        self.delete(
            '/api/admin/users/%d/' % self.user_b.id
        )
        self.status(401)

        self.get(
            '/api/admin/users/export/',
        )
        self.status(401)

        self.get(
            '/api/admin/users/staff/'
        )
        self.status(401)

        self.get(
            '/api/admin/users/staff/%d/' % self.staff.id
        )
        self.status(401)

        self.patch(
            '/api/admin/users/staff/%d/' % self.staff.id
        )
        self.status(401)

        self.delete(
            '/api/admin/users/staff/%d/' % self.staff.id
        )
        self.status(401)

        self.create_user()

        self.patch(
            '/api/admin/users/%d/' % self.user_b.id,
            {
                'call_name': 'B'
            },
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/admin/users/%d/' % self.user_a.id,
            auth=True
        )
        self.status(403)

        self.get(
            '/api/admin/users/export/',
            auth=True
        )
        self.status(403)

        self.get(
            '/api/admin/users/staff/',
            auth=True
        )
        self.status(403)

        self.get(
            '/api/admin/users/staff/%d/' % self.staff.id,
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/admin/users/staff/%d/' % self.staff.id,
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/admin/users/staff/%d/' % self.staff.id,
            auth=True
        )
        self.status(403)

    def test_user_admin_result(self):
        self.patch(
            '/api/admin/users/%d/' % self.user_a.id,
            {
                'first_name': 'B',
                'last_name': 'Boy',
                'call_name': 'B-Boy',
                'tel': '+82 10 1234 5678',
                'address': '3245 146th PL SE'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('first_name'), 'B')
        self.check(self.data.get('last_name'), 'Boy')
        self.check(self.data.get('call_name'), 'B-Boy')
        self.check(self.data.get('tel'), '+82 10 1234 5678')
        self.check(self.data.get('address'), '3245 146th PL SE')

        self.delete(
            '/api/admin/users/%d/' % self.user_b.id,
            auth=True
        )
        self.status(200)

        self.get(
            '/api/admin/users/export/',
            auth=True
        )
        self.status(200)
        self.check(
            self.response.headers.get('Content-Type'),
            Const.MIME_TYPE_XLSX
        )

    def test_users_admin_staff(self):
        self.get(
            '/api/admin/users/staff/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)

        self.patch(
            '/api/admin/users/staff/%d/' % self.staff.id,
            {
                'username': 'staff@a.com',
                'first_name': 'staff',
                'last_name': 'stephen',
                'call_name': 'st',
                'is_active': True,
                'is_staff': True,
                'is_superuser': False,
                'date_joined': '2021-12-31T09:00:00+0900'
            },
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/admin/users/staff/%d/' % self.staff.id,
            {
                'first_name': 'step',
                'is_superuser': True
            },
            auth=True
        )
        self.status(200)

        self.get(
            '/api/admin/users/staff/%d/' % self.staff.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('username'), 'staff@a.com')
        self.check(self.data.get('first_name'), 'step')
        self.check(self.data.get('last_name'), 'stephen')
        self.check(self.data.get('call_name'), 'st')
        self.check(self.data.get('is_active'))
        self.check(self.data.get('is_staff'))
        self.check(self.data.get('is_superuser'))
        self.check(self.data.get('date_joined'), '2021-12-31T09:00:00+0900')

        self.delete(
            '/api/admin/users/staff/%d/' % self.staff.id,
            auth=True
        )
        self.status(200)


class UserAdminListTest(TestCase):
    def setUp(self):
        self.buser = self.create_user(
            username='buser'
        )
        self.auser = self.create_user(
            username='auser'
        )
        self.cuser = self.create_user(
            username='cuser'
        )
        self.staff = self.create_user(is_staff=True)

    def test_users_admin_sorting(self):
        self.get(
            '/api/admin/users/?q=user',
            auth=True
        )
        self.check(self.data[0].get('id'), self.cuser.id)
        self.check(self.data[1].get('id'), self.auser.id)
        self.check(self.data[2].get('id'), self.buser.id)

        self.get(
            '/api/admin/users/?sort=username_dsc',
            auth=True
        )
        self.check(self.data[0].get('id'), self.cuser.id)
        self.check(self.data[1].get('id'), self.buser.id)
        self.check(self.data[2].get('id'), self.auser.id)

        self.get(
            '/api/admin/users/?sort=username_asc',
            auth=True
        )
        self.check(self.data[0].get('id'), self.auser.id)
        self.check(self.data[1].get('id'), self.buser.id)
        self.check(self.data[2].get('id'), self.cuser.id)

        self.get(
            '/api/admin/users/?sort=earliest',
            auth=True
        )
        self.check(self.data[0].get('id'), self.buser.id)
        self.check(self.data[1].get('id'), self.auser.id)
        self.check(self.data[2].get('id'), self.cuser.id)

        self.get(
            '/api/admin/users/?sort=latest',
            auth=True
        )
        self.check(self.data[0].get('id'), self.cuser.id)
        self.check(self.data[1].get('id'), self.auser.id)
        self.check(self.data[2].get('id'), self.buser.id)
