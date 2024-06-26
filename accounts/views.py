from django.conf import settings
from django.utils import timezone

from core.error import Error
from core.viewsets import (
    APIView,
    CreateAPIView,
    GenericAPIView,
    ModelViewSet
)
from core.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated
)
from core.response import Response
from core.wrapper import async_func
from utils.constants import Const
from utils.datautils import true_or_false
from utils.debug import Debug  # noqa
from utils.email import EmailHelper
from utils.excel import ExcelViewSet
from utils.sms import SMSHelper
from utils.text import Text
from utils.netutils import get_ip_address, get_user_agent

from . import (
    models,
    serializers,
    tools
)


class UserSignupView(CreateAPIView):
    serializer_class = serializers.SignupSerializer
    permission_classes = [AllowAny]


class UserLoginView(GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]

    def get_iam_serializer(self):
        if settings.USE_LOGIN_DEVICE:
            serializer = serializers.LoginDeviceIAMSerializer
        else:
            serializer = serializers.UserIAMSerializer
        return serializer

    def login(self, request, user):
        if settings.USE_LOGIN_DEVICE:
            ip_address = get_ip_address(request)
            device, os, browser = get_user_agent(request)

            login_device, _ = models.LoginDevice.objects.get_or_create(
                user=user,
                device=device,
                os=os,
                browser=browser,
                ip_address=ip_address
            )
            key = login_device.user.key()
        else:
            login_device = None
            key = user.key()

        tools.set_last_login(login_device, user)

        data = {
            'key': key,
            'user': user,
            'login_device': login_device,
        }
        return data

    def post(self, request, *args, **kwargs):
        self.request_log(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = self.login(request, serializer.validated_data.get('user'))
        iam_serializer = self.set_serializer(self.get_iam_serializer(), data)
        return Response(iam_serializer.data)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if settings.USE_LOGIN_DEVICE:
            ip_address = get_ip_address(request)
            device, os, browser = get_user_agent(request)

            login_device = models.LoginDevice.objects.filter(
                user=request.user,
                device=device,
                os=os,
                browser=browser,
                ip_address=ip_address
            ).first()
            tools.delete_device(login_device)
        else:
            tools.delete_auth_token(request.user)

        return Response(status=Response.HTTP_200)


class DeactivateAccountView(GenericAPIView):
    serializer_class = serializers.DeactivateAccountSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if settings.USE_LOGIN_DEVICE:
            models.LoginDevice.objects.filter(user=request.user).delete()

        tools.deactivate_account(request.user, models.AuthCode)
        return Response(status=Response.HTTP_200)


class LoginDeviceViewSet(ModelViewSet):
    serializer_class = serializers.LoginDeviceSerializer
    model = models.LoginDevice
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if settings.USE_LOGIN_DEVICE:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(user=self.request.user)
        else:
            return self.model.objects.none()

    def register(self, request, *args, **kwargs):
        instance = self.get_object()
        if tools.is_same_device(request, instance):
            tools.register_device(instance)
            return Response(status=Response.HTTP_200)
        else:
            return Response(status=Response.HTTP_400)


class PasswordChangeView(GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    sensitive_parameters = [
        'old_password',
        'new_password',
    ]


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    sensitive_parameters = [
        'new_password',
    ]


class UserSettingViewSet(ModelViewSet):
    serializer_class = serializers.UserSettingSerializer
    model = models.User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ConnectView(UserLoginView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = self.login(request, request.user)
        iam_serializer = self.set_serializer(self.get_iam_serializer(), data)
        return Response(iam_serializer.data)


class _UserAdminViewSet(ModelViewSet):
    serializer_class = serializers.IAmSerializer
    model = models.User
    permission_classes = [IsAdminUser]
    sort_option = {
        Const.QUERY_PARAM_USERNAME_DSC: '-username',
        Const.QUERY_PARAM_USERNAME_ASC: 'username',
    }

    def get_filters(self):
        return self.model.objects.query_active(self.request.query_params)

    def get_queryset(self):
        return self.model.objects.search(
            self.q, self.get_filters()
        ).order_by(self.get_order())

    def perform_delete(self, instance):
        if settings.USE_LOGIN_DEVICE:
            models.LoginDevice.objects.filter(user=instance).delete()
        tools.deactivate_account(instance, models.AuthCode)


class UserAdminViewSet(_UserAdminViewSet):
    serializer_class = serializers.UserAdminSerializer

    def get_filters(self):
        return self.model.objects.query_anti_staff(self.request.query_params)


class StaffAdminViewSet(_UserAdminViewSet):
    serializer_class = serializers.StaffAdminSerializer

    def get_filters(self):
        return self.model.objects.query_staff(self.request.query_params)


class UserAdminExportViewSet(UserAdminViewSet, ExcelViewSet):
    filename_prefix = 'user'
    title = [
        'id',
        '%s' % Text.EXCEL_TITLE_USERNAME,
        '%s' % Text.EXCEL_TITLE_FIRSTNAME,
        '%s' % Text.EXCEL_TITLE_LASTNAME,
        '%s' % Text.EXCEL_TITLE_CALLNAME,
        '%s' % Text.EXCEL_TITLE_TEL,
        '%s' % Text.EXCEL_TITLE_ADDRESS,
        '%s' % Text.EXCEL_TITLE_ACTIVE,
        '%s' % Text.EXCEL_TITLE_APPROVED,
        '%s' % Text.EXCEL_TITLE_JOINED_DATE,
    ]

    def make_data(self, key=None, index=0):
        data = [
            self.title
        ]
        format_data = [
            self.header_format
        ]

        for user in key:
            user_data = [
                user.get('id'),
                user.get('username'),
                self.get_not_null(user.get('first_name')),
                self.get_not_null(user.get('last_name')),
                self.get_not_null(user.get('call_name')),
                self.get_not_null(user.get('tel')),
                self.get_not_null(user.get('address')),
                self.get_not_null(user.get('is_active')),
                self.get_not_null(user.get('is_approved')),
                user.get('date_joined').split('T')[0],
            ]
            data.append(user_data)
            format_data.append(self.content_format)

        return data, format_data


class AuthCodeViewSet(ModelViewSet):
    serializer_class = serializers.AuthCodeSerializer
    model = models.AuthCode
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.all()

    def save_serializer(self, serializer):
        return serializer.save()

    def send_message(self, user, instance):
        pass

    def perform_create(self, serializer):
        instance = self.save_serializer(serializer)
        instance.code = tools.generate_auth_code()

        self.language = Text.language()
        self.send_message(self.request.user, instance)

        instance.save()


class SMSAuthViewSet(AuthCodeViewSet):
    serializer_class = serializers.SMSAuthSerializer

    @async_func
    def send_message(self, user, instance):
        Text.activate(self.language)
        msg = Text.MSG_SMS_AUTHENTICATE % {
            'code': instance.code
        }

        SMSHelper.send(
            instance.tel,
            msg
        )


class EmailAuthViewSet(AuthCodeViewSet):
    serializer_class = serializers.EmailAuthSerializer

    def save_serializer(self, serializer):
        return serializer.save(email=self.request.user.username)

    @async_func
    def send_message(self, user, instance):
        Text.activate(self.language)

        EmailHelper.send(
            subject='email_auth_subject.txt',
            html_subject='email_auth_subject.txt',
            body='email_auth.html',
            to=user.username,
            html_body='email_auth.html',
            context={
                'site_name': settings.SITE_NAME,
                'call_name': user.call_name,
                'auth_code': instance,
            }
        )


class AuthCodeAnswerViewSet(AuthCodeViewSet):
    serializer_class = serializers.AuthCodeAnswerSerializer

    def answer(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        now = timezone.localtime()
        code = request.data.get('code')

        if instance.is_used:
            Error.used_auth_code()

        if now > instance.expired_at():
            Error.expired_auth_code()

        if code != instance.code:
            instance.wrong_input = code
            instance.is_used = True
            instance.used_at = now
            instance.save()

            Error.invalid_auth_code()

        instance.is_used = True
        instance.used_at = now
        instance.save()

        tools.approve_user(request.user, instance)
        return Response(serializer.data)


class AuthCodeAdminViewSet(AuthCodeViewSet):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        used = true_or_false(
            self.request.query_params.get(Const.QUERY_PARAM_USED)
        )
        success = true_or_false(
            self.request.query_params.get(Const.QUERY_PARAM_SUCCESS)
        )
        return self.model.objects.search(self.q, used, success)
