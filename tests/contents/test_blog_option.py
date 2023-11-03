from utils.constants import Const
from contents.tests import TestCase


class BlogOptionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_option_permission(self):
        self.get(
            '/api/contents/blog_option/'
        )
        self.status(200)

        self.patch(
            '/api/contents/blog_option/'
        )
        self.status(401)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blog_option/',
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/contents/blog_option/',
            auth=True
        )
        self.status(403)

    def test_blog_option_check_fields(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'title': 'blog',
                'description': 'my blog',
                'category': [
                    'a',
                    'b'
                ],
                'option': {
                    'permission_list': Const.PERMISSION_ALL,
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_ALL,
                    'permission_reply': Const.PERMISSION_MEMBER,
                    'permission_vote': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'blog')
        self.check(self.data.get('description'), 'my blog')
        self.check(self.data.get('category'), ['a', 'b'])

        option = self.data.get('option')
        self.check(option.get('permission_list'), Const.PERMISSION_ALL)
        self.check(option.get('permission_read'), Const.PERMISSION_ALL)
        self.check(option.get('permission_write'), Const.PERMISSION_STAFF)
        self.check(option.get('permission_reply'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_vote'), Const.PERMISSION_ALL)

        self.patch(
            '/api/contents/blog_option/',
            {
                'title': 'blog2',
                'category': ['c'],
                'option': {
                    'permission_read': 'member'
                }
            },
            auth=True
        )
        self.get(
            '/api/contents/blog_option/',
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'blog2')
        self.check(self.data.get('description'), 'my blog')
        self.check(self.data.get('category'), ['c'])

        option = self.data.get('option')
        self.check(option.get('permission_list'), Const.PERMISSION_ALL)
        self.check(option.get('permission_read'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_write'), Const.PERMISSION_STAFF)
        self.check(option.get('permission_reply'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_vote'), Const.PERMISSION_ALL)
