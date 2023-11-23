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
    path(
        'blog/', views.BlogWriteViewSet.as_view({
            'post': 'create',
        }), name='new_blog'
    ),
    path(
        'blog/<int:pk>/', views.BlogUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='edit_blog'
    ),
    path(
        'blogs/', views.BlogViewSet.as_view({
            'get': 'list',
        }), name='blogs'
    ),
    path(
        'blogs/<int:pk>/', views.BlogReadViewSet.as_view({
            'get': 'retrieve',
        }), name='read_blog'
    ),
    path(
        'blogs/<int:pk>/like/', views.BlogLikeViewSet.as_view({
            'post': 'like',
        }), name='like_blog'
    ),
    path(
        'blogs/<int:pk>/comment/', views.CommentViewSet.as_view({
            'post': 'create',
        }), name='comment'
    ),
    path(
        'comment/<int:pk>/', views.CommentUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'delete',
        }), name='edit_comment'
    ),
]
