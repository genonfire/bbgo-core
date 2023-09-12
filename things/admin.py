from django.contrib import admin

from . import models


@admin.register(models.Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'content_type',
        'size',
        'created_at',
    )
    search_fields = (
        'file',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'file',
    )


class OrderThingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'order',
        'thing_type',
    )
    search_fields = (
        'name',
    )
    ordering = (
        'order',
        'id',
    )
    list_display_links = (
        'name',
    )
