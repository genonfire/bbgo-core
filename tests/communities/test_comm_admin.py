from communities.tests import TestCase


class ThreadAdminTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.forum1 = self.create_forum()
        self.create_thread(title='hi')

    def test_check_permission(self):
        self.create_user(username='user@a.com')

        self.get(
            '/api/admin/threads/'
        )
        self.status(401)

        self.get(
            '/api/admin/threads/',
            auth=True
        )
        self.status(403)

    def test_thread_admin_list(self):
        self.forum2 = self.create_forum(name='forum2')
        self.create_thread(title='hi', up_users=[self.user])
        hello1 = self.create_thread(title='hello')
        hello2 = self.create_thread(title='hello', is_pinned=True)
        hello3 = self.create_thread(title='hello', is_deleted=True)

        self.get(
            '/api/admin/threads/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 5)

        self.get(
            '/api/admin/threads/?q=hi',
            auth=True
        )
        self.check(len(self.data), 2)
        thread_id = self.data[1].get('id')

        self.get(
            '/api/admin/threads/?q=hi&sort=earliest',
            auth=True
        )
        self.check(len(self.data), 2)
        self.check(self.data[0].get('id'), thread_id)

        self.get(
            '/api/admin/threads/?q=hello',
            auth=True
        )
        self.check(len(self.data), 3)

        self.get(
            '/api/admin/threads/?q=hello&delete=true',
            auth=True
        )
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), hello3.id)

        self.get(
            '/api/admin/threads/?q=hello&delete=True&pin=true',
            auth=True
        )
        self.check(len(self.data), 0)

        self.get(
            '/api/admin/threads/?q=hello&delete=False&pin=True',
            auth=True
        )
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), hello2.id)

        self.get(
            '/api/admin/threads/?q=hello&delete=false&pin=false',
            auth=True
        )
        self.check(len(self.data), 1)
        self.check(self.data[0].get('id'), hello1.id)


class ReplyAdminTest(TestCase):
    def setUp(self):
        self.create_user(is_staff=True)
        self.forum1 = self.create_forum()
        self.create_thread(title='hi')
        self.create_reply()

    def test_check_permission(self):
        self.create_user(username='user@a.com')

        self.get(
            '/api/admin/replies/'
        )
        self.status(401)

        self.get(
            '/api/admin/replies/',
            auth=True
        )
        self.status(403)

    def test_thread_admin_list(self):
        self.forum2 = self.create_forum(name='forum2')
        self.create_thread(title='hi')
        hello1 = self.create_thread(title='hello')
        hello2 = self.create_thread(title='hello', is_pinned=True)

        self.create_reply(thread=hello1, content='hi')
        self.create_reply(thread=hello2, content='hi')
        self.create_reply(thread=hello2, content='hello', is_deleted=True)

        self.get(
            '/api/admin/replies/',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 4)

        self.get(
            '/api/admin/replies/?deleted=true&q=hello',
            auth=True
        )
        self.status(200)
        self.check(len(self.data), 1)

        self.get(
            '/api/admin/replies/?deleted=false&q=hi',
            auth=True
        )
        self.check(len(self.data), 2)
        reply_id = self.data[0].get('id')

        self.get(
            '/api/admin/replies/?deleted=false&q=hi&sort=earliest',
            auth=True
        )
        self.check(len(self.data), 2)
        self.check(self.data[1].get('id'), reply_id)
