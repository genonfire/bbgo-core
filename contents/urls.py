from django.urls import path

from . import views

app_name = 'contents'

urlpatterns = [
    path(
        'blog_option/', views.BlogOptionViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
        }), name='blog_option'
    ),
]
