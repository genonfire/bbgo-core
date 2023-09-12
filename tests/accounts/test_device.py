from django.conf import settings

from accounts.tests import TestCase
from utils.datautils import search_dict


class DeviceTest(TestCase):
    def setUp(self):
        settings.USE_LOGIN_DEVICE = True

        self.create_user()
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )
        self.login_device = self.data.get('login_device')

    def test_device_register(self):
        self.check_not(self.login_device.get('is_registered'))

        device_id = self.login_device.get('id')
        self.post(
            '/api/accounts/device/%d/register/' % device_id,
            auth=True
        )
        self.status(200)

        self.get(
            '/api/accounts/devices/',
            auth=True
        )
        device = search_dict('id', device_id, self.data)
        self.check(device.get('is_registered'))

    def test_device_register_different_device(self):
        device_id = self.login_device.get('id')
        self.client = self.get_client('PC')
        self.post(
            '/api/accounts/login/',
            {
                'username': self.username,
                'password': self.password
            }
        )

        self.post(
            '/api/accounts/device/%d/register/' % device_id,
            auth=True
        )
        self.status(400)

    def test_device_delete(self):
        device_id = self.login_device.get('id')
        self.delete(
            '/api/accounts/device/%d/delete/' % device_id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/accounts/devices/',
            auth=True
        )
        self.check_not(self.data)

    def test_device_logout(self):
        self.post(
            '/api/accounts/logout/',
            auth=True
        )
        self.status(200)

        self.get(
            '/api/accounts/devices/',
            auth=True
        )
        self.check_not(self.data)
