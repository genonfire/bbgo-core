from communities.tests import TestCase


class ForumPermissionTest(TestCase):
    def setUp(self):
        self.create_user()

    def test_forum_create_permission(self):
        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(403)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            format='json'
        )
        self.status(401)


class ForumCreateTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_forum_null_name(self):
        self.post(
            '/api/communities/forum/',
            {
                'name': '',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'name': None,
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

    def test_forum_validate_fields(self):
        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'anonymous',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegally smolcats',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats1',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(201)

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats1',
                'option': {
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(400)

    def test_forum_create_basic(self):
        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {
                    'is_active': True,
                    'permission_read': 'all',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(201)

        option = self.data.get('option')
        managers = self.data.get('managers')
        self.check(self.data.get('name'), 'illegallysmolcats')
        self.check(self.data.get('title'), 'Illegally Small Cats')
        self.check(self.data.get('description'), 'why so small')
        self.check(option.get('permission_read'), 'all')
        self.check(option.get('permission_write'), 'staff')
        self.check(option.get('permission_reply'), 'member')
        self.check(managers[0].get('id'), self.user.id)


class ForumEditTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_edit_forum_option(self):
        self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'option': {
                    'permission_read': 'member',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(200)

        option = self.data.get('option')
        self.check(option.get('permission_read'), 'member')
        self.check(option.get('permission_write'), 'staff')
        self.check(option.get('permission_reply'), 'member')
        self.check(option.get('is_active'), self.forum.is_active())

    def test_edit_forum_managers(self):
        user = self.user
        self.create_user(
            username='111@a.com',
            is_staff=True
        )

        self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'managers': [
                    {
                        'id': user.id
                    },
                    {
                        'id': self.user.id
                    }
                ]
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('managers')[0].get('id'), self.user.id)
        self.check(self.data.get('managers')[1].get('id'), user.id)

    def test_edit_forum_all_fields(self):
        self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'name': 'test',
                'title': 'test',
                'description': 'test',
                'option': {
                    'is_active': False,
                    'permission_read': 'member',
                    'permission_write': 'staff',
                    'permission_reply': 'member'
                }
            },
            auth=True
        )
        self.status(200)

        option = self.data.get('option')
        self.check(self.data.get('name'), self.forum.name)
        self.check(self.data.get('title'), 'test')
        self.check(self.data.get('description'), 'test')
        self.check(option.get('permission_read'), 'member')
        self.check(option.get('permission_write'), 'staff')
        self.check(option.get('permission_reply'), 'member')
        self.check_not(option.get('is_active'))


class ForumDeleteTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()

    def test_delete_forum(self):
        self.delete(
            '/api/communities/forum/%d/' % self.forum.id,
            auth=True
        )
        self.status(204)

        self.get(
            '/api/communities/forums/%d/' % self.forum.id,
            auth=True
        )
        self.status(404)


class ForumListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_get_forums(self):
        sample_name = [
            'black',
            'white',
            'red',
            'blue',
            'purple',
        ]
        sample_title = [
            'tiger',
            'blackcat',
            'dragon',
            'fish',
            'snake',
        ]
        forum_list = []
        for index in range(5):
            forum = self.create_forum(
                name=sample_name[index],
                title=sample_title[index]
            )
            forum_list.append(forum)

        self.get(
            '/api/communities/forums/',
            auth=True
        )

        for index, forum in enumerate(reversed(forum_list)):
            self.check(self.data[index].get('id'), forum.id)
            self.check(self.data[index].get('name'), forum.name)
            self.check(self.data[index].get('title'), forum.title)
            self.check(self.data[index].get('thread_count'), 0)
            self.check(self.data[index].get('reply_count'), 0)

        self.get(
            '/api/communities/forums/?q=black',
            auth=True
        )
        self.status(200)
        self.check_in('black', self.data[0].get('title'))
        self.check_in('black', self.data[1].get('name'))
