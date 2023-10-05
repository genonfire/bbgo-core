from django.urls import path

from accounts import views as accounts_views
from communities import views as communities_views


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
]
