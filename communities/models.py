from django.db import models
from django.db.models import (
    Case,
    IntegerField,
    Q,
    When,
)
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa


class OptionManager(models.Manager):
    pass


class Option(models.Model):
    is_active = models.BooleanField(default=True)
    permission_read = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    permission_write = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    permission_reply = models.CharField(
        max_length=Const.FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )

    objects = OptionManager()

    class Meta:
        ordering = ['id']


class ForumManager(models.Manager):
    def search(self, q):
        if q:
            query = (
                Q(name__icontains=q) |
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(managers__username__iexact=q)
            )
        else:
            query = Q()
        return self.filter(query).distinct()


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
    option = models.ForeignKey(
        'Option',
        related_name='forum_option',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(default=timezone.now)

    objects = ForumManager()

    class Meta:
        ordering = ['-id']

    def thread_count(self):
        return Thread.objects.forum(self).count()

    def reply_count(self):
        return Reply.objects.filter(thread__forum=self).count()

    def is_active(self):
        return self.option.is_active


class ThreadManager(models.Manager):
    def forum(self, forum, user=None):
        if isinstance(forum, Forum):
            return self.filter(forum=forum).filter(is_deleted=False)
        elif user and user.is_staff:
            return self.filter(forum__name=forum)
        else:
            return self.filter(forum__name=forum).filter(is_deleted=False)

    def search(self, forum, q):
        if q:
            query = (
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                (Q(user__isnull=True) & Q(name__icontains=q)) |
                Q(user__call_name__icontains=q)
            )
        else:
            query = Q()
        return self.forum(forum).filter(query).distinct()

    def deleted(self, forum):
        if isinstance(forum, Forum):
            return self.filter(forum=forum).filter(is_deleted=True)
        else:
            return self.filter(forum__name=forum).filter(is_deleted=True)

    def trash(self, forum, q):
        if q:
            query = (
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(name__icontains=q) |
                Q(user__username__icontains=q)
            )
        else:
            query = Q()
        return self.deleted(forum).filter(query)


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
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = ThreadManager()

    class Meta:
        ordering = ['-is_pinned', '-id']

    def forum_name(self):
        if self.forum:
            return self.forum.name
        else:
            return None

    def date_or_time(self):
        today = timezone.localtime()
        modified_at = timezone.localtime(self.modified_at)

        if modified_at.date() == today.date():
            return {
                'date': None,
                'time': modified_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
            }
        else:
            return {
                'date': modified_at.date(),
                'time': None,
            }


class ReplyManager(models.Manager):
    def thread(self, thread):
        if isinstance(thread, Thread):
            thread_replies = Q(thread=thread)
        else:
            thread_replies = Q(thread__id=thread)

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


class Reply(models.Model):
    thread = models.ForeignKey(
        'Thread',
        related_name='reply_thread',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    reply_id = models.IntegerField(default=0)
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
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)

    objects = ReplyManager()

    class Meta:
        ordering = ['-id']

    def forum(self):
        if self.thread:
            return self.thread.forum
        else:
            return None

    def date_or_time(self):
        today = timezone.localtime()
        modified_at = timezone.localtime(self.modified_at)

        if modified_at.date() == today.date():
            return {
                'date': None,
                'time': modified_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
            }
        else:
            return {
                'date': modified_at.date(),
                'time': None,
            }
