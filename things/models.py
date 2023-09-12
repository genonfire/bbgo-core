from django.db import models
from django.db.models import Q
from django.utils import timezone

from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.file import (
    generate_filename,
    get_original_filename,
)


def app_directory_path(instance, filename):
    return 'files/%s' % generate_filename(filename)


class AttachmentManager(models.Manager):
    def search(self, q):
        filename = Q()
        if q:
            filename = Q(file__icontains=q)
        return self.filter(filename)


class Attachment(models.Model):
    file = models.FileField(
        upload_to=app_directory_path,
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    content_type = models.CharField(
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    objects = AttachmentManager()

    class Meta:
        ordering = ['-id']

    def filename(self):
        return get_original_filename(self.file.url)


class OrderThingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            thing_type=self.model._meta.verbose_name
        )

    def things_name(self, name):
        if name:
            name_filter = Q(name=name)
        else:
            name_filter = Q()
        return self.filter(name_filter)


class OrderThing(models.Model):
    thing_type = models.CharField(
        max_length=Const.NAME_MAX_LENGTH
    )
    order = models.IntegerField(default=Const.BASE_ORDER)
    name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )

    objects = OrderThingManager()

    class Meta:
        ordering = ['order', 'id']
