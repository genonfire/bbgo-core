from django.urls import path

from . import views

app_name = 'communities'

urlpatterns = [
    path(
        'forum/', views.ForumViewSet.as_view({
            'post': 'create',
        }), name='new_forum'
    ),
    path(
        'forum/<int:pk>/', views.ForumUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='forum'
    ),
    path(
        'forums/', views.ForumReadOnlyViewSet.as_view({
            'get': 'list',
        }), name='forums'
    ),
    path(
        'forums/<int:pk>/', views.ForumReadOnlyViewSet.as_view({
            'get': 'retrieve',
        }), name='retrieve_forum'
    ),
    path(
        'f/<str:forum>/write/', views.ThreadViewSet.as_view({
            'post': 'create',
        }), name='new_thread'
    ),
    path(
        'f/<str:forum>/<int:pk>/', views.ThreadUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'delete',
        }), name='thread'
    ),
    path(
        'f/<str:forum>/<int:pk>/pin/', views.ThreadToggleViewSet.as_view({
            'post': 'pin',
        }), name='pin_thread'
    ),
    path(
        'f/<str:forum>/<int:pk>/unpin/', views.ThreadToggleViewSet.as_view({
            'post': 'unpin',
        }), name='unpin_thread'
    ),
    path(
        'f/<str:forum>/<int:pk>/restore/', views.ThreadRestoreViewSet.as_view({
            'post': 'restore',
        }), name='restore_thread'
    ),
    path(
        'f/<str:forum>/read/<int:pk>/', views.ThreadReadOnlyViewSet.as_view({
            'get': 'retrieve',
        }), name='retrieve_thread'
    ),
    path(
        'f/<str:forum>/', views.ThreadListViewSet.as_view({
            'get': 'list',
        }), name='threads'
    ),
    path(
        'f/<str:forum>/trash/', views.ThreadTrashViewSet.as_view({
            'get': 'list',
        }), name='threads_trash'
    ),
    path(
        'f/<int:pk>/reply/', views.ReplyViewSet.as_view({
            'post': 'create',
        }), name='reply'
    ),
    path(
        'r/<int:pk>/', views.ReplyUpdateViewSet.as_view({
            'patch': 'partial_update',
            'delete': 'delete',
        }), name='update_reply'
    ),
    path(
        'f/<int:pk>/replies/', views.ReplyListViewSet.as_view({
            'get': 'list',
        }), name='replies'
    ),
]
