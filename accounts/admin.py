from django.contrib import admin
from django.conf import settings
from django.contrib.auth.models import Group
from rest_framework.authtoken import (
    admin as token_admin,
    models as token_models,
)

from . import models


admin.sites.site.unregister(Group)
admin.sites.site.unregister(token_models.TokenProxy)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'call_name',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
    )
    search_fields = (
        'id',
        'username',
        'call_name',
        'first_name',
        'last_name',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'username',
        'call_name',
    )


if settings.USE_LOGIN_DEVICE:
    @admin.register(models.LoginDevice)
    class LoginDeviceAdmin(admin.ModelAdmin):
        list_display = (
            'id',
            'user',
            'device',
            'os',
            'browser',
            'ip_address',
            'last_login',
            'is_registered',
        )
        search_fields = (
            'id',
            'user',
            'ip_address',
        )
        ordering = (
            '-id',
        )
        list_display_links = (
            'id',
            'user',
            'device',
        )


@admin.register(models.AuthCode)
class AuthCodeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'tel',
        'code',
        'is_used',
        'wrong_input',
        'created_at',
        'tried_at',
    )
    search_fields = (
        'email',
        'tel',
    )
    ordering = (
        '-id',
    )
    list_display_links = (
        'id',
        'email',
        'tel',
    )


@admin.register(token_models.Token)
class TokenAdmin(token_admin.TokenAdmin):
    search_fields = (
        'key',
        'user__username',
    )
