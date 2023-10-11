from django.core.files.uploadedfile import SimpleUploadedFile

from core.testcase import TestCase as CoreTestCase
from utils.constants import Const

from . import models


class TestCase(CoreTestCase):
    def file(
        self,
        name='test.txt',
        content=b'test',
        content_type='text/plain'
    ):
        return SimpleUploadedFile(name, content, content_type)

    def create_option(
        self,
        permission_read=None,
        permission_write=None,
        permission_reply=None,
        permission_vote=None,
        support_files=False
    ):
        self.option = Const.FORUM_OPTION_DEFAULT

        if permission_read:
            self.option['permission_read'] = permission_read
        if permission_write:
            self.option['permission_write'] = permission_write
        if permission_reply:
            self.option['permission_reply'] = permission_reply
        if permission_vote:
            self.option['permission_vote'] = permission_vote
        if support_files:
            self.option['support_files'] = support_files

        return self.option

    def create_forum(
        self,
        name='illegallysmolcats',
        title='Illegally Small Cats',
        description='Why so small',
        managers=None,
        option=None,
        is_active=True
    ):
        if not option:
            option = self.create_option()

        self.forum = models.Forum.objects.create(
            name=name,
            title=title,
            description=description,
            option=option,
            is_active=is_active
        )
        if managers:
            for manager in managers:
                self.forum.managers.add(manager)
        else:
            self.forum.managers.add(self.user)
        return self.forum

    def create_thread(
        self,
        forum=None,
        user=None,
        name=None,
        title='Hello',
        content='Kitty',
        is_pinned=False,
        is_deleted=False,
        up_users=[],
        down_users=[]
    ):
        if not forum:
            forum = self.forum
        if not user and not name:
            user = self.user

        self.thread = models.Thread.objects.create(
            forum=forum,
            user=user,
            name=name,
            title=title,
            content=content,
            is_pinned=is_pinned,
            is_deleted=is_deleted
        )

        if up_users:
            for up_user in up_users:
                self.thread.up_users.add(up_user.id)

        if down_users:
            for down_user in down_users:
                self.thread.down_users.add(down_user.id)

        return self.thread

    def create_reply(
        self,
        thread=None,
        reply_id=0,
        user=None,
        name=None,
        content='Meow',
        is_deleted=False,
        up_users=[],
        down_users=[]
    ):
        if not thread:
            thread = self.thread
        if not user and not name:
            user = self.user

        self.reply = models.Reply.objects.create(
            thread=thread,
            reply_id=reply_id,
            user=user,
            name=name,
            content=content,
            is_deleted=is_deleted
        )

        if up_users:
            for up_user in up_users:
                self.reply.up_users.add(up_user.id)

        if down_users:
            for down_user in down_users:
                self.reply.down_users.add(down_user.id)

        return self.reply
