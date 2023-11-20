from contents.tests import TestCase
from utils.constants import Const


class BlogUpdatePermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_permission_update_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_write': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.create_blog()

        self.create_user(username='staff@a.com', is_staff=True)
        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.create_user(username='member@a.com')
        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
        )
        self.status(401)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
        )
        self.status(401)

    def test_blog_permission_update_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_write': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

        self.create_blog()

        self.create_user(username='staff@a.com', is_staff=True)
        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.create_user(username='member@a.com')
        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
        )
        self.status(401)

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
        )
        self.status(401)


class BlogUpdateTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                    'hobby',
                    'asmr'
                ],
                'option': {
                    'permission_write': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.post(
            '/api/things/file/',
            {
                'file': self.png(name='thumbnail.png')
            },
            format='multipart',
            auth=True
        )
        self.thumbnail_id = self.data.get('id')

    def test_blog_update_check_fields_by_staff(self):
        self.post(
            '/api/contents/blog/',
            {
                'title': 'test',
                'content': 'hi',
                'category': 'asmr',
                'image': {
                    'id': self.thumbnail_id
                },
                'tags': 'asmr, hobby',
                'is_published': True
            },
            auth=True
        )
        blog_id = self.data.get('id')

        self.patch(
            '/api/contents/blog/%d/' % blog_id,
            {
                'title': 'test2',
                'content': 'hello',
                'category': 'hobby',
                'image': None,
                'tags': None,
                'is_published': False
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'test2')
        self.check(self.data.get('content'), 'hello')
        self.check(self.data.get('category'), 'hobby')
        self.check_not(self.data.get('image'))
        self.check_not(self.data.get('tags'))
        self.check_not(self.data.get('is_published'))

        self.delete(
            '/api/contents/blog/%d/' % blog_id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/contents/blogs/%d/' % blog_id,
            auth=True
        )
        self.status(404)


class BlogUpdateTestMember(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

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

        self.post(
            '/api/things/file/',
            {
                'file': self.png(name='thumbnail.png')
            },
            format='multipart',
            auth=True
        )
        self.thumbnail_id = self.data.get('id')

    def test_blog_update_check_fields_by_member(self):
        self.create_user(username='blogger@a.com')
        self.create_blog(
            title='test2',
            content='hello',
            category='hobby',
        )

        self.patch(
            '/api/contents/blog/%d/' % self.blog.id,
            {
                'image': {
                    'id': self.thumbnail_id
                },
                'tags': 'hobby, asmr'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'test2')
        self.check(self.data.get('content'), 'hello')
        self.check(self.data.get('category'), 'hobby')
        self.check(self.data.get('image').get('id'), self.thumbnail_id)
        self.check(self.data.get('tags'), 'hobby, asmr')
        self.check(self.data.get('is_published'))

        self.delete(
            '/api/contents/blog/%d/' % self.blog.id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)
