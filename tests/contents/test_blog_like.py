from contents.tests import TestCase
from utils.constants import Const


class BlogLikePermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_permission_vote_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_vote': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )
        self.create_blog()

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
        )
        self.status(401)

        self.create_user('member@a.com')
        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(403)

        self.create_user('staff@a.com', is_staff=True)
        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(400)

    def test_blog_permission_vote_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_vote': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )
        self.create_blog()

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
        )
        self.status(401)

        self.create_user('staff@a.com', is_staff=True)
        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.create_blog()
        self.create_user('member@a.com')

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
            auth=True
        )
        self.status(400)

    def test_blog_permission_vote_all(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_vote': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )
        blog1 = self.create_blog()
        blog2 = self.create_blog()
        blog3 = self.create_blog()

        self.post(
            '/api/contents/blogs/%d/like/' % blog1.id,
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/like/' % blog1.id,
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/like/' % blog1.id,
        )
        self.status(400)

        self.create_user('member@a.com')
        self.post(
            '/api/contents/blogs/%d/like/' % blog2.id,
            auth=True
        )
        self.status(200)

        self.create_user('staff@a.com', is_staff=True)
        self.post(
            '/api/contents/blogs/%d/like/' % blog3.id,
            auth=True
        )
        self.status(200)


class BlogLikeTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_list': Const.PERMISSION_ALL,
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_vote': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )
        self.create_blog()

    def test_blog_like_result(self):
        self.post(
            '/api/contents/blogs/%d/like/' % self.blog.id,
        )
        self.status(200)
        self.check(self.data.get('like'), 1)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
        )
        self.check(self.data.get('like'), 1)
        self.check(self.data.get('liked'))
