"""bbgo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from utils.bot import (
    DailyBotView,
    MinuteBotView,
    MonthlyBotView,
)


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('bot/daily/', DailyBotView.as_view(), name='daily_bot'),
    path('bot/monthly/', MonthlyBotView.as_view(), name='monthly_bot'),
    path('bot/minute/', MinuteBotView.as_view(), name='minute_bot'),
    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path(
        'api/communities/',
        include('communities.urls', namespace='communities')
    ),
    path('api/things/', include('things.urls', namespace='things')),
    path('api/admin/', include('bbgo.admin_urls')),
    prefix_default_language=False
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.LOCAL_SERVER:
    urlpatterns += [
        path(
            'restapi/',
            include('rest_framework.urls', namespace='rest_framework')
        )
    ]

    if 'drf_yasg' in settings.INSTALLED_APPS:
        from rest_framework import permissions
        from drf_yasg.views import get_schema_view
        from drf_yasg import openapi

        schema_view = get_schema_view(
            openapi.Info(
                title="bbgo APIs",
                default_version='beta',
            ),
            public=True,
            permission_classes=[permissions.AllowAny],
        )
        urlpatterns += [
            re_path(
                r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0),
                name='schema-json'
            ),
            re_path(
                r'^swagger/$',
                schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'
            ),
            re_path(
                r'^redoc/$',
                schema_view.with_ui('redoc', cache_timeout=0),
                name='schema-redoc'
            ),
        ]
