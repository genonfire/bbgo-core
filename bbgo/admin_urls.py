from django.urls import path

from accounts import views as accounts_views
from communities import views as communities_views
from contents import views as contents_views
from things import views as things_views


urlpatterns = [
    path(
        'users/', accounts_views.UserAdminViewSet.as_view({
            'get': 'list',
        }), name='users'
    ),
    path(
        'users/<int:pk>/', accounts_views.UserAdminViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'delete'
        }), name='user_admin'
    ),
    path(
        'users/export/', accounts_views.UserAdminExportViewSet.as_view({
            'get': 'list',
        }), name='user_export'
    ),
    path(
        'users/staff/', accounts_views.StaffAdminViewSet.as_view({
            'get': 'list',
        }), name='staff_list'
    ),
    path(
        'users/staff/<int:pk>/', accounts_views.StaffAdminViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'delete'
        }), name='staff'
    ),
    path(
        'auth_codes/', accounts_views.AuthCodeAdminViewSet.as_view({
            'get': 'list',
        }), name='auth_codes'
    ),
    path(
        'auth_codes/<int:pk>/', accounts_views.AuthCodeAdminViewSet.as_view({
            'get': 'retrieve',
        }), name='auth_code'
    ),
    path(
        'threads/', communities_views.ThreadAdminViewSet.as_view({
            'get': 'list',
        }), name='threads'
    ),
    path(
        'replies/', communities_views.ReplyAdminViewSet.as_view({
            'get': 'list',
        }), name='replies'
    ),
    path(
        'blogs/', contents_views.BlogAdminListViewSet.as_view({
            'get': 'list',
        }), name='blogs'
    ),
    path(
        'blogs/<int:pk>/', contents_views.BlogAdminViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy'
        }), name='blog'
    ),
    path(
        'comments/', contents_views.CommentAdminViewSet.as_view({
            'get': 'list',
        }), name='comments'
    ),
    path(
        'comments/<int:pk>/',
        contents_views.CommentAdminDeleteViewSet.as_view({
            'delete': 'delete'
        }), name='delete_comment'
    ),
    path(
        'comments/restore/<int:pk>/',
        contents_views.CommentAdminRestoreViewSet.as_view({
            'post': 'restore'
        }), name='restore_comment'
    ),
    path(
        'files/', things_views.AttachmentManageViewSet.as_view({
            'get': 'list',
        }), name='files'
    ),
]
