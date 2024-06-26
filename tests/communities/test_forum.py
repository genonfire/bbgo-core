from communities.tests import TestCase
from utils.constants import Const


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
                'is_active': True,
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
                },
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
                'is_active': True,
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                'is_active': True,
                'option': {
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                'is_active': False,
                'option': {
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                'is_active': True,
                'option': {
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                'is_active': True
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
                'is_active': True,
                'option': {
                    'permission_read': 'anonymous',
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
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
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER
                }
            },
            auth=True
        )
        self.status(400)

    def test_forum_create_basic(self):
        manager_member = self.create_user(username='member@a.com')
        manager_staff = self.create_user(
            username='staff@a.com',
            is_staff=True
        )
        manager_list = [
            manager_member.id,
            manager_staff.id
        ]

        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'is_active': False,
                'managers': [
                    {
                        'id': manager_member.id
                    },
                    {
                        'id': manager_staff.id
                    }
                ],
                'option': {
                    'permission_list': Const.PERMISSION_ALL,
                    'permission_read': Const.PERMISSION_ALL,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER,
                    'permission_vote': Const.PERMISSION_ALL,
                }
            },
            auth=True
        )
        self.status(201)

        self.check(self.data.get('name'), 'illegallysmolcats')
        self.check(self.data.get('title'), 'Illegally Small Cats')
        self.check(self.data.get('description'), 'why so small')
        self.check_not(self.data.get('is_active'))

        option = self.data.get('option')
        self.check(option.get('permission_list'), Const.PERMISSION_ALL)
        self.check(option.get('permission_read'), Const.PERMISSION_ALL)
        self.check(option.get('permission_write'), Const.PERMISSION_STAFF)
        self.check(option.get('permission_reply'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_vote'), Const.PERMISSION_MEMBER)

        managers = self.data.get('managers')
        self.check(len(managers), 2)
        for manager in managers:
            self.check_in(manager.get('id'), manager_list)

        self.get(
            '/api/communities/f/illegallysmolcats/seek/',
            auth=True
        )
        self.status(200)
        self.check(self.data.get('name'), 'illegallysmolcats')
        self.check(self.data.get('title'), 'Illegally Small Cats')
        self.check(self.data.get('description'), 'why so small')

        permissions = self.data.get('permissions')
        self.check(permissions.get('write'), True)
        self.check(permissions.get('reply'), True)
        self.check(permissions.get('vote'), True)

        managers = self.data.get('managers')
        self.check(len(managers), 2)
        for manager in managers:
            self.check_in(manager.get('id'), manager_list)

    def test_forum_create_check_default_option(self):
        self.post(
            '/api/communities/forum/',
            {
                'name': 'illegallysmolcats',
                'title': 'Illegally Small Cats',
                'description': 'why so small',
                'option': {}
            },
            auth=True
        )
        self.status(201)

        option = self.data.get('option')
        managers = self.data.get('managers')
        self.check(self.data.get('name'), 'illegallysmolcats')
        self.check(self.data.get('title'), 'Illegally Small Cats')
        self.check(self.data.get('description'), 'why so small')
        self.check(self.data.get('is_active'))
        self.check(
            option.get('permission_read'),
            Const.FORUM_OPTION_DEFAULT.get('permission_read')
        )
        self.check(
            option.get('permission_write'),
            Const.FORUM_OPTION_DEFAULT.get('permission_write')
        )
        self.check(
            option.get('permission_reply'),
            Const.FORUM_OPTION_DEFAULT.get('permission_reply')
        )
        self.check(
            option.get('permission_vote'),
            Const.FORUM_OPTION_DEFAULT.get('permission_vote')
        )
        self.check(option.get('support_files'), False)
        self.check(managers[0].get('id'), self.user.id)


class ForumEditTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_option()
        self.create_forum()

    def test_edit_forum(self):
        self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'option': {
                    'permission_read': Const.PERMISSION_MEMBER,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER,
                    'permission_vote': Const.PERMISSION_ALL,
                    'support_files': True
                }
            },
            auth=True
        )
        self.status(200)

        option = self.data.get('option')
        self.check(option.get('permission_read'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_write'), Const.PERMISSION_STAFF)
        self.check(option.get('permission_reply'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_vote'), Const.PERMISSION_MEMBER)
        self.check(option.get('support_files'))

        self.patch(
            '/api/communities/forum/%d/' % self.forum.id,
            {
                'name': 'test',
                'title': 'test',
                'description': 'test',
                'is_active': False,
                'option': {
                    'permission_read': Const.PERMISSION_MEMBER,
                    'permission_write': Const.PERMISSION_STAFF,
                    'permission_reply': Const.PERMISSION_MEMBER,
                    'permission_vote': Const.PERMISSION_STAFF,
                    'support_files': True
                },
            },
            auth=True
        )
        self.status(200)

        option = self.data.get('option')
        self.check(self.data.get('name'), self.forum.name)
        self.check(self.data.get('title'), 'test')
        self.check(self.data.get('description'), 'test')
        self.check_not(self.data.get('is_active'))
        self.check(option.get('permission_read'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_write'), Const.PERMISSION_STAFF)
        self.check(option.get('permission_reply'), Const.PERMISSION_MEMBER)
        self.check(option.get('permission_vote'), Const.PERMISSION_STAFF)
        self.check(option.get('support_files'))

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


class ForumDeleteTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_option()
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
        self.create_option()

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
        sample_active = [
            False,
            True,
            True,
            False,
            True,
        ]
        forum_list = []
        for index in range(5):
            forum = self.create_forum(
                name=sample_name[index],
                title=sample_title[index],
                is_active=sample_active[index]
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
            self.check(self.data[index].get('is_active'), forum.is_active)
            self.check(self.data[index].get('thread_count'), 0)
            self.check(self.data[index].get('reply_count'), 0)

        self.get(
            '/api/communities/forums/?q=black',
            auth=True
        )
        self.status(200)
        self.check_in('black', self.data[0].get('title'))
        self.check_in('black', self.data[1].get('name'))

        self.get(
            '/api/communities/forums/?q=black&active=False',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)

        self.get(
            '/api/communities/forums/?&active=true',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 3)
