from contents.tests import TestCase
from utils.constants import Const


class BlogCommentPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_blog_permission_comment_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.create_blog()

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
        )
        self.status(401)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'name': 'guest',
                'content': 'test',
            }
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='guest@a.com')
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': self.data.get('id'),
                'content': 'test',
            },
            auth=True
        )
        self.status(403)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(403)

    def test_blog_permission_comment_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_MEMBER,
                    'permission_reply': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

        self.create_blog()

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
        )
        self.status(401)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'name': 'guest',
                'content': 'test',
            }
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='guest@a.com')
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': self.data.get('id'),
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(200)

    def test_blog_permission_comment_all(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_reply': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )

        self.create_blog()

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'content': 'test',
            }
        )
        self.status(400)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'name': 'guest',
                'content': 'test',
            }
        )
        self.status(201)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': self.data.get('id'),
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.create_user(username='guest@a.com')
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'content': 'test',
            },
            auth=True
        )
        self.status(201)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.status(200)


class BlogCommentTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_reply': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )

        self.create_blog()
        self.create_comment()

    def test_blog_comment_check_fields(self):
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'name': 'guest',
            }
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'name': 'guest',
                'content': None,
            }
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'commnet_id': self.comment.id,
                'content': '',
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': self.comment.id,
                'name': 'guest',
                'content': 'hi',
            }
        )
        self.status(201)
        self.check(self.data.get('blog').get('id'), self.blog.id)
        self.check(self.data.get('comment_id'), self.comment.id)
        self.check_not(self.data.get('user'))
        self.check(self.data.get('name'), 'guest')
        self.check(self.data.get('content'), 'hi')
        self.check_not(self.data.get('is_deleted'))
        self.check_not(self.data.get('date_or_time').get('date'))

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'content': 'hello',
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('blog').get('id'), self.blog.id)
        self.check(self.data.get('comment_id'), 0)
        self.check(self.data.get('user').get('id'), self.user.id)
        self.check_not(self.data.get('name'))
        self.check(self.data.get('content'), 'hello')
        self.check_not(self.data.get('is_deleted'))

    def test_comment_update_permission(self):
        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            }
        )
        self.status(401)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
        )
        self.status(401)

        self.create_user(username='guest@a.com')
        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
            auth=True
        )
        self.status(404)

        self.create_user(username='staff@a.com', is_staff=True)
        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.create_comment(
            name='guest'
        )

        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'name': 'guest',
                'content': 'bye'
            }
        )
        self.status(401)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
        )
        self.status(401)

        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

    def test_comment_edit_delete(self):
        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('comment_id'), 0)
        self.check(self.data.get('user').get('id'), self.user.id)
        self.check_not(self.data.get('name'))
        self.check(self.data.get('content'), 'bye')
        self.check_not(self.data.get('is_deleted'))
        self.check_not(self.data.get('date_or_time').get('date'))

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': self.comment.id,
                'content': 'hi',
            },
            auth=True
        )
        comment_id = self.data.get('id')

        self.patch(
            '/api/contents/comment/%d/' % comment_id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('comment_id'), self.comment.id)
        self.check(self.data.get('user').get('id'), self.user.id)
        self.check_not(self.data.get('name'))
        self.check(self.data.get('content'), 'bye')
        self.check_not(self.data.get('is_deleted'))

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/contents/comment/%d/' % self.comment.id,
            {
                'content': 'bye'
            },
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/contents/comment/%d/' % self.comment.id,
            auth=True
        )
        self.status(404)

    def test_comment_to_invalid_id(self):
        self.create_blog()
        blog_id = int(self.blog.id) + 1

        self.post(
            '/api/contents/blogs/%d/comment/' % blog_id,
            {
                'content': 'hello',
            },
            auth=True
        )
        self.status(404)

        self.create_comment()
        comment_id = int(self.comment.id) + 1

        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': comment_id,
                'content': 'hello',
            },
            auth=True
        )
        self.status(404)


class CommentListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_reply': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.create_blog()

    def test_comment_list(self):
        comment = self.create_comment(content='A')
        self.create_comment(content='D')
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': comment.id,
                'content': 'B'
            },
            auth=True
        )
        nested_comment_id = self.data.get('id')

        self.create_comment(content='E')
        self.post(
            '/api/contents/blogs/%d/comment/' % self.blog.id,
            {
                'comment_id': nested_comment_id,
                'content': 'C'
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.check(len(self.data), 5)
        self.check(self.data[0].get('content'), 'A')
        self.check(self.data[0].get('comment_id'), 0)
        self.check(self.data[1].get('content'), 'B')
        self.check(self.data[1].get('comment_id'), comment.id)
        self.check(self.data[2].get('content'), 'C')
        self.check(self.data[2].get('comment_id'), comment.id)
        self.check(self.data[3].get('content'), 'D')
        self.check(self.data[3].get('comment_id'), 0)
        self.check(self.data[4].get('content'), 'E')
        self.check(self.data[4].get('comment_id'), 0)

        self.delete(
            '/api/contents/comment/%d/' % comment.id,
            auth=True
        )
        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id,
            auth=True
        )
        self.check(len(self.data), 5)

        self.get(
            '/api/contents/blogs/%d/comments/' % self.blog.id
        )
        self.check(len(self.data), 4)
