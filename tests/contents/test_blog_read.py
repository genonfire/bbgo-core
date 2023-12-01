from contents.tests import TestCase
from utils.constants import Const


class BlogReadPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_list': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )
        self.create_blog()

    def test_blog_permission_list_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_list': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/',
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(403)

    def test_blog_permission_list_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_list': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/',
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)

    def test_blog_permission_list_all(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_list': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/',
        )
        self.status(200)

        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)

    def test_blog_permission_read_staff(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_STAFF,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(403)

    def test_blog_permission_read_member(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
        )
        self.status(401)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)

    def test_blog_permission_read_all(self):
        self.patch(
            '/api/contents/blog_option/',
            {
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
        )
        self.status(200)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)

        self.create_user(username='blogger@a.com')
        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(200)


class BlogListTest(TestCase):
    def setUp(self):
        self.staff = self.create_user(is_staff=True)
        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                    'breakfast',
                    'lunch',
                    'supper',
                ],
                'option': {
                    'permission_list': Const.PERMISSION_MEMBER,
                }
            },
            auth=True
        )

    def test_blog_list(self):
        sample_title = [
            'sugar',
            'salt',
            'chili',
            'vinegar',
            'msg',
        ]
        sample_content = [
            'sweet',
            'salty',
            'spicy',
            'sour',
            'tasty',
        ]
        sample_category = [
            '',
            'breakfast',
            'lunch',
            'supper',
            '',
        ]
        sample_tags = [
            'spice',
            'pepper',
            'spice, pepper',
            'pepper, spice, msg',
            '',
        ]
        blog_list = []
        for index in range(5):
            blog = self.create_blog(
                title=sample_title[index],
                content=sample_content[index],
                category=sample_category[index],
                tags=sample_tags[index],
            )
            blog_list.append(blog)

        self.get(
            '/api/contents/blogs/',
            auth=True
        )

        for index, blog in enumerate(reversed(blog_list)):
            self.check(self.data[index].get('id'), blog.id)
            self.check(self.data[index].get('title'), blog.title)
            self.check(self.data[index].get('category'), blog.category)
            self.check(self.data[index].get('tags'), blog.tags)

        self.get(
            '/api/contents/blogs/?category=lunch',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('title'), 'chili')

        self.get(
            '/api/contents/blogs/?tag=pepper',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 3)
        self.check(self.data[0].get('title'), 'vinegar')
        self.check(self.data[1].get('title'), 'chili')
        self.check(self.data[2].get('title'), 'salt')

        self.get(
            '/api/contents/blogs/?tag=pepper&q=chili',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('title'), 'chili')

        self.get(
            '/api/contents/blogs/?category=lunch&tag=pepper&q=spic',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('title'), 'chili')

    def test_blog_draft_list(self):
        self.create_blog(
            title='draft',
            is_published=False
        )

        self.get(
            '/api/contents/blogs/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 0)

        self.get(
            '/api/contents/blogs/?q=draft',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 0)

        self.create_blog(
            tags='draft',
            is_published=True
        )

        self.get(
            '/api/contents/blogs/?q=draft',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)


class BlogReadTest(TestCase):
    def setUp(self):
        self.jake = self.create_user(username='jake@a.com', is_staff=True)

        self.patch(
            '/api/contents/blog_option/',
            {
                'category': [
                    'food',
                ],
                'option': {
                    'permission_list': Const.PERMISSION_STAFF,
                    'permission_read': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )
        self.create_blog()

    def test_blog_read_draft(self):
        self.create_blog(is_published=False)

        self.get(
            '/api/contents/blogs/%d/' % self.blog.id,
            auth=True
        )
        self.status(404)

        self.get(
            '/api/contents/blogs/%d/' % int(self.blog.id + 1),
            auth=True
        )
        self.status(404)

    def test_blog_read_published(self):
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
                'title': 'hungry',
                'content': 'nyam',
                'category': 'food',
                'image': {
                    'id': thumbnail_id
                },
                'tags': 'food, lunch, supper',
                'is_published': True
            },
            auth=True
        )

        self.get(
            '/api/contents/blogs/%d/' % self.data.get('id'),
            auth=True
        )
        self.status(200)
        self.check(self.data.get('user').get('username'), 'jake@a.com')
        self.check(self.data.get('title'), 'hungry')
        self.check(self.data.get('content'), 'nyam')
        self.check(self.data.get('category'), 'food')
        self.check(self.data.get('image').get('id'), thumbnail_id)
        self.check(self.data.get('tags'), 'food, lunch, supper')
        self.check(self.data.get('like'), 0)
        self.check(self.data.get('is_published'))
        self.check(self.data.get('editable'))

        self.get(
            '/api/contents/blogs/%d/' % self.data.get('id'),
        )
        self.status(200)
        self.check_not(self.data.get('editable'))

        self.create_user(username='member@a.com')
        self.get(
            '/api/contents/blogs/%d/' % self.data.get('id'),
            auth=True
        )
        self.status(200)
        self.check_not(self.data.get('editable'))
