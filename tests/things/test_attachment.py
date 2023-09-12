from utils.file import get_original_filename
from things.tests import TestCase


class FileUploadTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_attachment_upload_png(self):
        self.post(
            '/api/things/file/',
            {
                'file': self.png('image.png')
            },
            format='multipart',
            auth=True
        )
        self.status(201)
        self.check(self.data.get('content_type'), 'image/png')
        self.check(self.data.get('size'), 58)
        self.check_not(self.data.get('file'), 'image.png')
        self.check(
            get_original_filename(self.data.get('file')),
            'image.png'
        )
        self.check(self.data.get('filename'), 'image.png')

    def test_attachment_upload_same_file(self):
        self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )
        file = self.data

        self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )
        self.status(201)
        self.check_not(self.data.get('file'), file.get('file'))
        self.check(self.data.get('content_type'), file.get('content_type'))
        self.check(self.data.get('size'), file.get('size'))

    def test_attachment_upload_invalid_param(self):
        self.post(
            '/api/things/file/',
            {
            },
            format='multipart',
            auth=True
        )
        self.status(400)

        self.post(
            '/api/things/file/',
            {
                'file': ''
            },
            format='multipart',
            auth=True
        )
        self.status(400)

        self.post(
            '/api/things/file/',
            {
                'file': None
            },
            auth=True
        )
        self.status(400)

    def test_attachment_upload_max_size(self):
        data = 'R0lGODlhAQABAAD/ACwAAAAAAQABAAACAD'
        content = 'data:image/png;base64,' + data + data + data + 's='

        self.post(
            '/api/things/file/',
            {
                'file': self.png(content=content.encode('utf=8')),
            },
            format='multipart',
            auth=True
        )
        self.status(400)


class FilePermissionTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_attachment()

    def test_attachment_manage_permission(self):
        self.get(
            '/api/things/files/',
            auth=True
        )
        self.status(403)

    def test_attachment_delete_permission(self):
        self.post(
            '/api/things/file/',
            {
                'file': self.file()
            },
            format='multipart',
            auth=True
        )

        self.create_user(username='attacher@a.com')

        self.delete(
            '/api/things/file/%d/' % self.data.get('id'),
            auth=True
        )
        self.status(403)


class FileManageTest(TestCase):
    def setUp(self):
        self.create_user()
        self.create_attachment()
        self.create_user(username='admin@a.com', is_staff=True)
        self.create_attachment(name='attachment.txt')

    def test_attachment_list_and_delete(self):
        self.get(
            '/api/things/files/?q=attachment',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(
            get_original_filename(self.data[0].get('file')),
            'attachment.txt'
        )
        self.check(self.data[0].get('filename'), 'attachment.txt')

        self.get(
            '/api/things/files/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 2)

        self.delete(
            '/api/things/file/%d/' % self.data[1].get('id'),
            auth=True
        )
        self.status(204)

        self.get(
            '/api/things/files/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)

        self.delete(
            '/api/things/file/%d/' % self.data[0].get('id'),
            auth=True
        )
        self.status(204)

        self.get(
            '/api/things/files/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 0)
