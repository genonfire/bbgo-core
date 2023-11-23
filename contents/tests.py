from core.testcase import TestCase as CoreTestCase

from . import models


class TestCase(CoreTestCase):
    def create_blog(
        self,
        user=None,
        title='test',
        content='test',
        category=None,
        tags=None,
        like_users=None,
        is_published=True,
    ):
        if not user:
            user = self.user

        self.blog = models.Blog.objects.create(
            user=user,
            title=title,
            content=content,
            category=category,
            tags=tags,
            like_users=like_users,
            is_published=is_published
        )

        return self.blog

    def create_comment(
        self,
        blog=None,
        comment_id=0,
        user=None,
        name=None,
        content='Moo',
        is_deleted=False,
    ):
        if not blog:
            blog = self.blog
        if not user and not name:
            user = self.user

        self.comment = models.Comment.objects.create(
            blog=blog,
            comment_id=comment_id,
            user=user,
            name=name,
            content=content,
            is_deleted=is_deleted
        )

        return self.comment
