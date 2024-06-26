from communities.tests import TestCase
from utils.constants import Const


class ReplyPermissionTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_permission_reply_all(self):
        self.create_option(
            permission_read=Const.PERMISSION_ALL,
            permission_write=Const.PERMISSION_ALL,
            permission_reply=Const.PERMISSION_ALL
        )
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
        self.check_not(self.data[0].get('editable'))

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
            '/api/communities/f/%d/replies/' % thread_id,
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check(self.data[0].get('editable'))

        self.get(
            '/api/communities/f/%d/replies/' % thread_id
        )
        self.status(200)
        self.check(len(self.data), 1)
        self.check_not(self.data[0].get('editable'))

    def test_permission_reply_member(self):
        option = self.create_option(
            permission_read=Const.PERMISSION_ALL,
            permission_reply=Const.PERMISSION_MEMBER
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
            permission_read=Const.PERMISSION_ALL,
            permission_reply=Const.PERMISSION_STAFF
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
            permission_read=Const.PERMISSION_MEMBER,
            permission_reply=Const.PERMISSION_MEMBER
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
            permission_read=Const.PERMISSION_STAFF,
            permission_reply=Const.PERMISSION_STAFF
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
        self.create_option()
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

        self.get(
            '/api/communities/f/%s/' % self.forum.name,
            auth=True
        )
        self.check(self.data.get('threads')[0].get('reply_count'), 4)

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

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check(self.data.get('reply_count'), 1)

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

        self.get(
            '/api/communities/f/%s/read/%d/' % (
                self.forum.name, self.thread.id
            ),
            auth=True
        )
        self.check(self.data.get('reply_count'), 0)

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
        self.create_option()
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
        self.check(self.data[0].get('content'), '5')
        self.check(self.data[0].get('reply_id'), 0)
        self.check(self.data[1].get('content'), '4')
        self.check(self.data[1].get('reply_id'), 0)
        self.check(self.data[2].get('content'), '1')
        self.check(self.data[2].get('reply_id'), 0)
        self.check(self.data[3].get('content'), '2')
        self.check(self.data[3].get('reply_id'), reply_id)
        self.check(self.data[4].get('content'), '3')
        self.check(self.data[4].get('reply_id'), reply_id)

        self.delete(
            '/api/communities/r/%d/' % self.data[4].get('id'),
            auth=True
        )
        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        self.check(len(self.data), 5)

        self.create_user(username='replier@a.com')
        self.get(
            '/api/communities/f/%d/replies/' % self.thread.id,
            auth=True
        )
        self.check(len(self.data), 4)


class ReplyVoteTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)

    def test_reply_check_vote_user(self):
        self.create_option()
        self.create_forum()
        self.create_thread()
        self.create_reply()

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(400)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(400)

    def test_reply_check_vote_permission_staff(self):
        self.create_option(
            permission_vote=Const.PERMISSION_STAFF
        )
        self.create_forum()
        self.create_thread()
        self.create_reply()

        self.create_user(username='voter@a.com')
        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(403)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(403)

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id
        )
        self.status(401)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id
        )
        self.status(401)

    def test_reply_check_vote_permission_member(self):
        self.create_option(
            permission_vote=Const.PERMISSION_MEMBER
        )
        self.create_forum()
        self.create_thread()
        self.create_reply()

        self.create_user(username='voter@a.com')
        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(200)

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id
        )
        self.status(401)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id
        )
        self.status(401)

    def test_reply_check_vote_number(self):
        self.create_option(
            permission_vote=Const.PERMISSION_MEMBER
        )
        self.create_forum()
        self.create_thread()
        self.create_reply()

        self.create_user(username='upper@a.com')

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 1)
        self.check(self.data.get('down'), 0)

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 0)
        self.check(self.data.get('down'), 0)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 0)
        self.check(self.data.get('down'), 1)

        self.create_user(username='downer@a.com')

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 0)
        self.check(self.data.get('down'), 2)

        self.post(
            '/api/communities/r/%d/down/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 0)
        self.check(self.data.get('down'), 1)

        self.post(
            '/api/communities/r/%d/up/' % self.reply.id,
            auth=True
        )
        self.status(200)
        self.check(self.data.get('id'), self.reply.id)
        self.check(self.data.get('up'), 1)
        self.check(self.data.get('down'), 1)
