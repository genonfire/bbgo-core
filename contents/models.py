from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from utils.constants import Const


class BlogOption(models.Model):
    name = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        unique=True,
    )
    title = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True)
    category = ArrayField(
        models.CharField(
            max_length=Const.FIELD_MAX_LENGTH,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    option = models.JSONField(
        blank=True,
        null=True,
    )


class BlogManager(models.Manager):
    pass


class Blog(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='blog_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=Const.TITLE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    category = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    image = models.ForeignKey(
        'things.Attachment',
        related_name='blog_image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    tags = models.CharField(
        max_length=Const.DESC_MAX_LENGTH,
        blank=True,
        null=True,
    )
    like_users = ArrayField(
        models.CharField(
            max_length=Const.IP_ADDRESS_MAX_LENGTH,
            blank=True,
            null=True,
        ),
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = BlogManager()

    class Meta:
        ordering = ['-id']


class CommentManager(models.Manager):
    pass


class Comment(models.Model):
    blog = models.ForeignKey(
        'Blog',
        related_name='comment_blog',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    comment_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        'accounts.User',
        related_name='comment_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = CommentManager()

    class Meta:
        ordering = ['-id']
