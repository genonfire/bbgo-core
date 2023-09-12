from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path(
        'signup/', views.UserSignupView.as_view(),
        name='signup'
    ),
    path(
        'login/', views.UserLoginView.as_view(),
        name='login'
    ),
    path(
        'connect/', views.ConnectView.as_view(),
        name='connect'
    ),
    path(
        'logout/', views.UserLogoutView.as_view(),
        name='logout'
    ),
    path(
        'device/<int:pk>/register/', views.LoginDeviceViewSet.as_view({
            'post': 'register'
        }), name='register_device'
    ),
    path(
        'device/<int:pk>/delete/', views.LoginDeviceViewSet.as_view({
            'delete': 'destroy'
        }), name='delete_device'
    ),
    path(
        'devices/', views.LoginDeviceViewSet.as_view({
            'get': 'list'
        }), name='device'
    ),
    path(
        'password/change/', views.PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password/find/', views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password/reset/', views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'setting/', views.UserSettingViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
        }), name='setting'
    ),
    path(
        'deactivate/', views.DeactivateAccountView.as_view(),
        name='deactivate'
    ),
    path(
        'auth/sms/', views.SMSAuthViewSet.as_view({
            'post': 'create',
        }), name='sms_auth'
    ),
    path(
        'auth/email/', views.EmailAuthViewSet.as_view({
            'post': 'create',
        }), name='email_auth'
    ),
    path(
        'auth/<int:pk>/', views.AuthCodeAnswerViewSet.as_view({
            'post': 'answer',
        }), name='auth'
    ),
]
