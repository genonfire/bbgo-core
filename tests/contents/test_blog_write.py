from utils.constants import Const
from contents.tests import TestCase


class BlogWritePermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_permission_write_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_write': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
        )
        self.status(401)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='blogger@a.com')
        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(403)

    def test_blog_permission_write_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_write': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
        )
        self.status(401)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='blogger@a.com')
        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

    def test_blog_permission_write_all(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_write': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
        )
        self.status(401)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='blogger@a.com')
        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(403)


class BlogWriteTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_write_check_fields(self):
        self.patch(
            '/api/contents/blog_option/',
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': '',
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blog/',
            {
                'title': '',
                'content': 'test',
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blog/',
            {
                'content': 'test',
            },
            auth=True
        )
        self.status(400)

    def test_blog_write_check_category(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                    'hobby',
                    'asmr'
                ]
            },
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': 'asmr'
            },
            auth=True
        )
        self.status(201)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': ''
            },
            auth=True
        )
        self.status(201)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': 'hobby, asmr'
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': 'bsmr'
            },
            auth=True
        )
        self.status(400)

        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                ]
            },
            auth=True
        )

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': 'bsmr'
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'test',
                'category': None
            },
            auth=True
        )
        self.status(201)
        self.check_not(self.data.get('category'))

    def test_blog_write_check_result(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                    'hobby',
                    'asmr'
                ],
                'option': {
                    'permission_write': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )
        self.create_user(username='jane@a.com')

        self.post(
            '/api/things/file/',
            {
                'file': self.png(name='thumbnail.png')
            },
            format='multipart',
            auth=True
        )
        thumbnail_id = self.data.get('id')

        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'hi',
                'category': 'asmr',
                'image': {
                    'id': thumbnail_id
                },
                'tags': 'asmr, hobby',
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('user').get('username'), 'jane@a.com')
        self.check(self.data.get('title'), 'test')
        self.check(self.data.get('content'), 'hi')
        self.check(self.data.get('category'), 'asmr')
        self.check(self.data.get('image').get('id'), thumbnail_id)
        self.check(self.data.get('tags'), 'asmr, hobby')
