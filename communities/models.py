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


class ForumManager(models.Manager):
    def query_active(self, q):
        active = true_or_false(q.get(Const.QUERY_PARAM_ACTIVE))
        if active:
            return Q(is_active=active)
        else:
            return Q()

    def forum_query(self, q):
        search_query = Q()
        if q:
            search_query = (
                Q(name__icontains=q) |
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return search_query

    def search(self, q, filters):
        if not filters:
            filters = Q()

        return self.filter(filters).filter(self.forum_query(q)).distinct()


class Forum(models.Model):
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
        unique=True,
    )
    title = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    description = models.TextField(null=True, blank=True)
    managers = models.ManyToManyField(
        'accounts.User',
        related_name='forum_managers',
        default='',
        blank=True,
    )
    option = models.JSONField(
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = ForumManager()

    class Meta:
        ordering = ['-id']

    def thread_count(self):
        return Thread.objects.forum(self).count()

    def reply_count(self):
        return Reply.objects.filter(thread__forum=self).count()

    def support_files(self):
        return self.option.get('support_files')


class ThreadManager(models.Manager):
    def forum(self, forum, user=None):
        if isinstance(forum, Forum):
            return self.filter(forum=forum).filter(is_deleted=False)
        elif user and user.is_staff:
            return self.filter(forum__name=forum)
        else:
            return self.filter(forum__name=forum).filter(is_deleted=False)

    def search_query(self, q):
        if q:
            query = (
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                (Q(user__isnull=True) & Q(name__icontains=q)) |
                Q(user__call_name__icontains=q)
            )
        else:
            query = Q()
        return query

    def search(self, forum, q):
        return self.forum(forum).filter(self.search_query(q)).distinct()

    def deleted(self, forum):
        if isinstance(forum, Forum):
            return self.filter(forum=forum).filter(is_deleted=True)
        else:
            return self.filter(forum__name=forum).filter(is_deleted=True)

    def trash(self, forum, q):
        return self.deleted(forum).filter(self.search_query(q)).distinct()

    def admin_query(self, q):
        query = Q()
        deleted = true_or_false(q.get(Const.QUERY_PARAM_DELETED))
        if deleted:
            query = Q(is_deleted=deleted)

        pinned = true_or_false(q.get(Const.QUERY_PARAM_PINNED))
        if pinned:
            query &= Q(is_pinned=pinned)

        return query

    def admin_search(self, q, filters):
        return self.filter(filters).filter(self.search_query(q)).distinct()


class Thread(models.Model):
    forum = models.ForeignKey(
        'Forum',
        related_name='thread_forum',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        'accounts.User',
        related_name='thread_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # in case of anonymous
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    title = models.CharField(
        max_length=Const.TITLE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    up_users = models.ManyToManyField(
        'accounts.User',
        related_name='thread_up',
        default='',
        blank=True,
    )
    down_users = models.ManyToManyField(
        'accounts.User',
        related_name='thread_down',
        default='',
        blank=True,
    )
    files = models.ManyToManyField(
        'things.Attachment',
        related_name='thread_files',
        default='',
        blank=True,
    )
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True)

    objects = ThreadManager()

    class Meta:
        ordering = ['-is_pinned', '-id']

    def forum_name(self):
        if self.forum:
            return self.forum.name
        else:
            return None

    def date_or_time(self):
        return date_or_time(self.created_at)

    def up(self):
        return self.up_users.count()

    def down(self):
        return self.down_users.count()

    def reply_count(self):
        return Reply.objects.active_count(self)


class ReplyManager(models.Manager):
    def active(self):
        return self.filter(is_deleted=False)

    def active_count(self, thread):
        return self.active().filter(thread=thread).count()

    def thread(self, thread, user):
        if isinstance(thread, Thread):
            thread_replies = Q(thread=thread)
        else:
            thread_replies = Q(thread__id=thread)

        if not user.is_staff:
            thread_replies &= Q(is_deleted=False)

        replies = self.filter(thread_replies).annotate(
            custom_order=Case(
                When(reply_id=0, then='id'),
                default='reply_id',
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')
        return replies

    def my(self, user):
        if user and user.is_staff:
            return self.filter(is_deleted=False)
        else:
            return self.filter(user=user).filter(is_deleted=False)

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

    def admin_query(self, q):
        query = Q()
        deleted = true_or_false(q.get(Const.QUERY_PARAM_DELETED))
        if deleted:
            query = Q(is_deleted=deleted)

        return query

    def admin_search(self, q, filters):
        return self.filter(filters).filter(self.search_query(q)).distinct()


class Reply(models.Model):
    thread = models.ForeignKey(
        'Thread',
        related_name='reply_thread',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reply_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        'accounts.User',
        related_name='reply_user',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # in case of anonymous
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content = models.TextField(null=True, blank=True)
    up_users = models.ManyToManyField(
        'accounts.User',
        related_name='reply_up',
        default='',
        blank=True,
    )
    down_users = models.ManyToManyField(
        'accounts.User',
        related_name='reply_down',
        default='',
        blank=True,
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(blank=True, null=True)

    objects = ReplyManager()

    class Meta:
        ordering = ['-id']

    def forum(self):
        if self.thread:
            return self.thread.forum
        else:
            return None

    def forum_name(self):
        if self.thread:
            return self.thread.forum_name()
        else:
            return None

    def date_or_time(self):
        return date_or_time(self.created_at)

    def up(self):
        return self.up_users.count()

    def down(self):
        return self.down_users.count()
