from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def create_option(
        self,
        is_active=True,
        permission_read='all',
        permission_write='all',
        permission_reply='all'
    ):
        self.option = models.Option.objects.create(
            is_active=is_active,
            permission_read=permission_read,
            permission_write=permission_write,
            permission_reply=permission_reply
        )
        return self.option

    def create_forum(
        self,
        name='illegallysmolcats',
        title='Illegally Small Cats',
        description='Why so small',
        option=None
    ):
        if not option:
            option = self.create_option()

        self.forum = models.Forum.objects.create(
            name=name,
            title=title,
            description=description,
            option=option
        )
        self.forum.managers.add(self.user)
        return self.forum

    def create_thread(
        self,
        forum=None,
        user=None,
        name=None,
        title='Hello',
        content='Kitty'
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
            content=content
        )
        return self.thread

    def create_reply(
        self,
        thread=None,
        reply_id=0,
        user=None,
        name=None,
        content='Meow'
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
            content=content
        )
        return self.reply
