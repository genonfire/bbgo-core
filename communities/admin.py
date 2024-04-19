from django.contrib import admin

from . import models


@admin.register(models.Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'title',
        'is_active',
        'created_at',
    )
    search_fields = (
        'name',
        'title',
        'description',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'name',
        'title',
    )


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'user',
        'name',
        'forum_name',
        'is_pinned',
        'is_deleted',
        'created_at',
        'modified_at',
    )
    search_fields = (
        'title',
        'content',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'title',
    )


@admin.register(models.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'thread',
        'reply_id',
        'content',
        'is_deleted',
        'created_at',
    )
    search_fields = (
        'user',
        'name',
        'content',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'user',
        'name',
    )
