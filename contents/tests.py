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
