from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import (
    Case,
    IntegerField,
    Q,
    When,
)
from django.utils import timezone

from utils.constants import Const
from utils.datautils import true_or_false
from utils.dateutils import date_or_time
from utils.debug import Debug  # noqa


class BlogOptionManager(models.Manager):
    def get(self):
        return self.get_or_create(name=settings.SITE_NAME)[0]


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
        default=list,
        blank=True,
        null=True,
    )
    option = models.JSONField(
        blank=True,
        null=True,
    )

    objects = BlogOptionManager()


class BlogManager(models.Manager):
    def my(self, user):
        return self.filter(user=user)

    def published(self):
        return self.filter(is_published=True)

    def query_category(self, q):
        query = Q()
        category = q.get(Const.QUERY_PARAM_CATEGORY)
        tag = q.get(Const.QUERY_PARAM_TAG)

        if category:
            query = Q(category=category)
        if tag:
            query &= Q(tags__icontains=tag)

        return query

    def search_query(self, q):
        if q:
            query = (
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__icontains=q)
            )
        else:
            query = Q()

        return query

    def search(self, q, filters):
        return self.published().filter(filters).filter(
            self.search_query(q)
        ).distinct()

    def admin_query(self, q):
        query = self.query_category(q)
        draft = true_or_false(q.get(Const.QUERY_PARAM_DRAFT))

        if draft:
            query &= ~Q(is_published=draft)

        return query

    def admin_search(self, q, filters):
        return self.filter(filters).filter(self.search_query(q)).distinct()


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
        default=list,
        blank=True,
        null=True,
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = BlogManager()

    class Meta:
        ordering = ['-id']

    def like(self):
        if self.like_users:
            return len(self.like_users)
        else:
            return 0


class CommentManager(models.Manager):
    def my(self, user):
        if user and user.is_staff:
            return self.filter(is_deleted=False)
        else:
            return self.filter(user=user).filter(is_deleted=False)

    def active(self):
        return self.filter(is_deleted=False)

    def deleted(self):
        return self.filter(is_deleted=True)

    def blog(self, blog, user):
        if isinstance(blog, Blog):
            blog_comments = Q(blog=blog)
        else:
            blog_comments = Q(blog__id=blog)

        if not user.is_staff:
            blog_comments &= Q(is_deleted=False)

        comments = self.filter(blog_comments).annotate(
            custom_order=Case(
                When(comment_id=0, then='id'),
                default='comment_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')
        return comments

    def admin_query(self, q):
        query = Q()
        deleted = true_or_false(q.get(Const.QUERY_PARAM_DELETED))
        if deleted:
            query = Q(is_deleted=deleted)
        return query

    def search_query(self, q):
        if q:
            query = (
                Q(content__icontains=q) |
                (Q(user__isnull=True) & Q(name__icontains=q)) |
                Q(user__call_name__icontains=q)
            )
        else:
            query = Q()
        return query

    def admin_search(self, q, filters):
        return self.filter(filters).filter(self.search_query(q)).distinct()


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

    def date_or_time(self):
        return date_or_time(self.created_at)
