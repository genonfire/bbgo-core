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
        'f/<str:forum>/', views.ThreadListViewSet.as_view({
            'get': 'list',
        }), name='threads'
    ),
    path(
        'f/<str:forum>/seek/', views.ThreadSeekViewSet.as_view({
            'get': 'seek',
        }), name='seek_forum'
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
        'f/<str:forum>/<int:pk>/file/', views.ThreadFileViewSet.as_view({
            'post': 'attach_files',
            'delete': 'delete_files',
        }), name='thread_file'
    ),
    path(
        'f/<str:forum>/read/<int:pk>/', views.ThreadReadOnlyViewSet.as_view({
            'get': 'retrieve',
        }), name='retrieve_thread'
    ),
    path(
        'f/<str:forum>/pin/<int:pk>/', views.ThreadToggleViewSet.as_view({
            'post': 'pin',
        }), name='pin_thread'
    ),
    path(
        'f/<str:forum>/unpin/<int:pk>/', views.ThreadToggleViewSet.as_view({
            'post': 'unpin',
        }), name='unpin_thread'
    ),
    path(
        'f/<str:forum>/trash/', views.ThreadTrashViewSet.as_view({
            'get': 'list',
        }), name='threads_trash'
    ),
    path(
        'f/<str:forum>/restore/<int:pk>/', views.ThreadRestoreViewSet.as_view({
            'post': 'restore',
        }), name='restore_thread'
    ),
    path(
        'f/<str:forum>/up/<int:pk>/', views.ThreadVoteViewSet.as_view({
            'post': 'up',
        }), name='up_thread'
    ),
    path(
        'f/<str:forum>/down/<int:pk>/', views.ThreadVoteViewSet.as_view({
            'post': 'down',
        }), name='down_thread'
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
    path(
        'r/<int:pk>/up/', views.ReplyVoteViewSet.as_view({
            'post': 'up',
        }), name='up_reply'
    ),
    path(
        'r/<int:pk>/down/', views.ReplyVoteViewSet.as_view({
            'post': 'down',
        }), name='down_reply'
    ),
]
