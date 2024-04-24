from contents.tests import TestCase


class BlogAdminPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

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
        self.create_blog()

    def test_blog_permission_admin(self):
        self.get(
            '/api/admin/blogs/',
        )
        self.status(401)

        self.get(
            '/api/admin/blogs/%d/' % self.blog.id
        )
        self.status(401)

        self.patch(
            '/api/admin/blogs/%d/' % self.blog.id,
            {
                'is_published': False
            }
        )
        self.status(401)

        self.delete(
            '/api/admin/blogs/%d/' % self.blog.id
        )
        self.status(401)

        self.get(
            '/api/admin/blogs/',
            auth=True
        )
        self.status(200)

        self.get(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.patch(
            '/api/admin/blogs/%d/' % self.blog.id,
            {
                'is_published': False
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(204)

        self.create_user(username='member@a.com')

        self.get(
            '/api/admin/blogs/',
            auth=True
        )
        self.status(403)

        self.get(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/admin/blogs/%d/' % self.blog.id,
            {
                'is_published': False
            },
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(403)


class BlogAdminTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

        self.post(
            '/api/things/file/',
            {
                'file': self.png(name='thumbnail.png')
            },
            format='multipart',
            auth=True
        )
        self.thumbnail_id = self.data.get('id')

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

        self.create_blog()

    def test_blog_admin_check_result(self):
        self.create_user(username='staff@a.com', is_staff=True)

        self.patch(
            '/api/admin/blogs/%d/' % self.blog.id,
            {
                'title': 'hi',
                'content': 'hello world',
                'category': 'asmr',
                'tags': 'hello, world',
                'image': {
                    'id': self.thumbnail_id
                },
                'is_published': False
            },
            auth=True
        )
        self.status(200)

        self.get(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('title'), 'hi')
        self.check(self.data.get('content'), 'hello world')
        self.check(self.data.get('category'), 'asmr')
        self.check(self.data.get('tags'), 'hello, world')
        self.check(self.data.get('image').get('id'), self.thumbnail_id)
        self.check_not(self.data.get('is_published'))
        self.check(self.data.get('editable'))

        self.delete(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/admin/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)


class BlogAdminListTest(TestCase):
    def setUp(self):
        self.john = self.create_user(username='john@a.com', is_staff=True)
        self.jane = self.create_user(username='jane@a.com', is_staff=True)
        self.jake = self.create_user(username='jake@a.com', is_staff=True)
        self.create_user(is_staff=True)

        self.category = {
            'category': [
                'hobby',
                'asmr'
            ]
        }

        self.patch(
            '/api/contents/blog_option/',
            self.category,
            auth=True
        )

    def test_blog_admin_check_filter(self):
        self.get(
            '/api/admin/blogs/',
            auth=True
        )
        self.status(200)
        self.check(self.response.data.get('filter'), self.category)

    def test_blog_admin_list(self):
        sample_category = [
            'hobby',
            'hobby',
            'asmr',
            'asmr',
        ]
        sample_published = [
            False,
            True,
            True,
            False,
        ]
        sample_like = [
            [self.john],
            [self.jane, self.jake, self.john],
            [self.john, self.jake],
            [],
        ]
        blog_list = []

        for index in range(4):
            blog = self.create_blog(
                category=sample_category[index],
                is_published=sample_published[index],
                like_users=sample_like[index]
            )
            blog_list.append(blog)

        self.get(
            '/api/admin/blogs/?sort=like',
            auth=True
        )
        self.status(200)
        self.check(self.data[0].get('id'), blog_list[1].id)
        self.check(self.data[1].get('id'), blog_list[2].id)
        self.check(self.data[2].get('id'), blog_list[0].id)
        self.check(self.data[3].get('id'), blog_list[3].id)

        self.get(
            '/api/admin/blogs/?draft=True&category=hobby&sort=like',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), blog_list[0].id)

        self.get(
            '/api/admin/blogs/?draft=False&category=asmr',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), blog_list[2].id)


class CommentAdminPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

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
        self.create_blog()
        self.deleted_comment = self.create_comment(is_deleted=True)
        self.create_comment()

    def test_comment_permission_admin(self):
        self.get(
            '/api/admin/comments/'
        )
        self.status(401)

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id
        )
        self.status(401)

        self.post(
            '/api/admin/comments/%d/' % self.deleted_comment.id
        )
        self.status(401)

        self.get(
            '/api/admin/comments/',
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/admin/comments/restore/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.create_user(username='member@a.com')

        self.get(
            '/api/admin/comments/',
            auth=True
        )
        self.status(403)

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id,
            auth=True
        )
        self.status(403)

        self.post(
            '/api/admin/comments/restore/%d/' % self.deleted_comment.id,
            auth=True
        )
        self.status(403)


class CommentAdminTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

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

    def test_comment_admin_check_result(self):
        self.create_blog()
        self.create_comment()

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id,
            auth=True
        )
        self.status(404)

        self.post(
            '/api/admin/comments/restore/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/admin/comments/%d/' % self.comment.id,
            auth=True
        )
        self.status(200)

    def test_comment_admin_list(self):
        self.create_blog(content='trust')
        comment1 = self.create_comment(
            content='fall',
            is_deleted=True
        )
        self.create_comment(
            comment_id=self.comment.id,
            content='trust'
        )
        self.create_blog(content='fall')
        comment3 = self.create_comment(content='fall')

        self.get(
            '/api/admin/comments/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 3)
        self.check(self.data[0].get('content'), 'fall')
        self.check(self.data[1].get('content'), 'trust')
        self.check(self.data[2].get('content'), 'fall')

        self.get(
            '/api/admin/comments/?delete=true',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), comment1.id)

        self.get(
            '/api/admin/comments/?delete=false&q=fall',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), comment3.id)
