from communities.tests import TestCase


class ReplyPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_reply_all(self):
        self.create_forum()
        self.create_thread()
        thread_id = self.thread.id

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        self.status(201)
        self.check(self.data.get('thread').get('id'), thread_id)
        self.check(self.data.get('reply_id'), 0)
        self.check_not(self.data.get('user'))
        self.check(self.data.get('name'), 'tester')
        self.check(self.data.get('content'), 'test')
        self.check_not(self.data.get('is_deleted'))
        reply_id = self.data.get('id')

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('name'), 'tester')
        self.check(self.data[0].get('content'), 'test')

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit'
            },
        )
        self.status(401)

        self.delete(
            '/api/communities/r/%d/' % reply_id
        )
        self.status(401)

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        self.status(200)

        self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        self.status(200)

        self.create_user(username='2@a.com')

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        self.status(404)

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('thread').get('id'), thread_id)
        self.check(self.data.get('reply_id'), 0)
        self.check(self.data.get('user').get('id'), self.user.id)
        self.check(self.data.get('content'), 'test')
        self.check_not(self.data.get('is_deleted'))

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(200)
        self.check(len(self.data), 2)

    def test_permission_reply_member(self):
        option = self.create_option(
            permission_reply='member'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        self.status(401)

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(200)

        self.create_user(username='4@a.com')

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        reply_id = self.data.get('id')

        self.check(self.data.get('content'), 'test')
        self.check(self.data.get('user').get('username'), self.user.username)

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('content'), 'edit')

        self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        self.status(200)

    def test_permission_reply_staff(self):
        option = self.create_option(
            permission_reply='staff'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'name': 'tester',
                'content': 'test'
            }
        )
        self.status(401)

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(200)

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        reply_id = self.data.get('id')

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('content'), 'edit')

        self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        self.status(200)

        self.create_user(username='4@a.com')

        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        self.status(403)

        self.patch(
            '/api/communities/r/%d/' % reply_id,
            {
                'content': 'edit',
            },
            auth=True
        )
        self.status(404)

        self.delete(
            '/api/communities/r/%d/' % reply_id,
            auth=True
        )
        self.status(404)

    def test_permission_thread_read_member(self):
        option = self.create_option(
            permission_read='member',
            permission_reply='member'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(401)

        self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        self.status(200)

        self.create_user(username='2@a.com')
        self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        self.status(200)

    def test_permission_thread_read_staff(self):
        option = self.create_option(
            permission_read='staff',
            permission_reply='staff'
        )
        self.create_forum(option=option)
        self.create_thread()
        thread_id = self.thread.id

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(401)

        self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        self.status(200)

        self.create_user(username='2@a.com')
        self.get(
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        self.status(403)


class ReplyModelTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()
        self.create_thread()
        self.create_reply()

    def test_nested_reply(self):
        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('reply_id'), 0)

        reply_id = self.data.get('id')
        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': reply_id,
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('reply_id'), reply_id)

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': self.data.get('id'),
                'content': 'test'
            },
            auth=True
        )
        self.status(201)
        self.check(self.data.get('reply_id'), reply_id)

    def test_reply_edit_delete(self):
        self.patch(
            '/api/communities/r/%d/' % self.reply.id,
            {
                'content': 'bow wow'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('content'), 'bow wow')
        self.check(self.data.get('reply_id'), 0)
        self.check_not(self.data.get('name'))

        self.patch(
            '/api/communities/r/%d/' % self.reply.id,
            {
                'reply_id': self.reply.id,
                'name': 'dog',
                'content': 'meow'
            },
            auth=True
        )
        self.status(200)
        self.check(self.data.get('content'), 'meow')
        self.check(self.data.get('reply_id'), 0)
        self.check_not(self.data.get('name'))

        self.delete(
            '/api/communities/r/%d/' % self.reply.id,
            auth=True
        )
        self.status(200)

        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        self.check(len(self.data), 1)
        self.check(self.data[0].get('is_deleted'))

    def test_reply_to_invalid_id(self):
        thread_id = int(self.thread.id) + 1
        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'content': 'test'
            },
            auth=True
        )
        self.status(404)

        reply_id = int(self.reply.id) + 1
        self.post(
            '/api/communities/f/%d/reply/' % thread_id,
            {
                'reply_id': reply_id,
                'content': 'test'
            },
            auth=True
        )
        self.status(404)


class ReplyListTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.create_forum()
        self.create_thread()

    def test_reply_list(self):
        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '1'
            },
            auth=True
        )
        reply_id = self.data.get('id')

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '4'
            },
            auth=True
        )

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': reply_id,
                'content': '2'
            },
            auth=True
        )
        nested_reply_id = self.data.get('id')

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'content': '5'
            },
            auth=True
        )

        self.post(
            '/api/communities/f/%d/reply/' % self.thread.id,
            {
                'reply_id': nested_reply_id,
                'content': '3'
            },
            auth=True
        )

        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        self.check(len(self.data), 5)
        self.check(self.data[0].get('content'), '1')
        self.check(self.data[0].get('reply_id'), 0)
        self.check(self.data[1].get('content'), '2')
        self.check(self.data[1].get('reply_id'), reply_id)
        self.check(self.data[2].get('content'), '3')
        self.check(self.data[2].get('reply_id'), reply_id)
        self.check(self.data[3].get('content'), '4')
        self.check(self.data[3].get('reply_id'), 0)
        self.check(self.data[4].get('content'), '5')
        self.check(self.data[4].get('reply_id'), 0)
