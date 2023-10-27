from django.contrib import admin

from . import models


@admin.register(models.BlogOption)
class BlogOptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'title',
        'category',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'name',
        'title',
    )


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'category',
        'tags',
        'is_published',
        'created_at',
    )
    search_fields = (
        'title',
        'tags',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'title',
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'blog',
        'comment_id',
        'content',
        'is_deleted',
        'modified_at',
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
