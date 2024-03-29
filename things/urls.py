from django.urls import path

from . import views

app_name = 'things'

urlpatterns = [
    path(
        'file/', views.AttachmentViewSet.as_view({
            'post': 'create',
        }), name='file_upload'
    ),
    path(
        'file/<int:pk>/', views.AttachmentViewSet.as_view({
            'delete': 'destroy',
        }), name='file_delete'
    ),
]
