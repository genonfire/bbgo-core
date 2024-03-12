from django.conf import settings
from django.contrib.auth import (
    authenticate,
    password_validation
)
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers

from core.error import Error
from core.serializers import (
    ModelSerializer,
    Serializer
)
from core.wrapper import async_func
from utils.constants import Const
from utils.debug import Debug  # noqa
from utils.text import Text

from . import models, tools


class SignupSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'call_name',
        ]
        read_only_fields = [
            'call_name',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': Const.REQUIRED,
            'last_name': Const.REQUIRED,
        }

    def create(self, validated_data):
        request = self.context.get('request')

        call_name = tools.get_call_name(
            validated_data.get('first_name'),
            validated_data.get('last_name'),
            request.LANGUAGE_CODE,
        )

        user = self.Meta.model.objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('username'),
            password=validated_data.get('password'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            call_name=call_name,
            is_approved=settings.USER_DEFAULT_APPROVED,
        )
        return user


class LoginSerializer(Serializer):
    username = serializers.EmailField(max_length=Const.EMAIL_MAX_LENGTH)
    password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def authenticate(self, **kwargs):
        return authenticate(self.context.get('request'), **kwargs)

    def validate(self, attrs):
        user = self.authenticate(
            username=attrs.get('username'),
            password=attrs.get('password'),
        )

        if not user:
            Error.unable_to_login()

        attrs['user'] = user
        return attrs


class LoginDeviceSerializer(ModelSerializer):
    class Meta:
        model = models.LoginDevice
        fields = [
            'id',
            'device',
            'os',
            'browser',
            'ip_address',
            'last_login',
            'is_registered',
        ]


class _PasswordChangeSerializer(Serializer):
    def save(self):
        self.user.set_password(self.validated_data.get('new_password'))
        self.user.save(update_fields=['password'])
        self.user.token().delete()

        if settings.USE_LOGIN_DEVICE:
            devices = models.LoginDevice.objects.filter(user=self.user)
            devices.delete()


class PasswordChangeSerializer(_PasswordChangeSerializer):
    old_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)
    new_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def validate(self, attrs):
        if not self.user.check_password(attrs.get('old_password')):
            Error.invalid_password()

        if attrs.get('old_password') == attrs.get('new_password'):
            Error.same_password()

        password_validation.validate_password(
            attrs.get('new_password'), self.user)

        return attrs


class PasswordResetConfirmSerializer(_PasswordChangeSerializer):
    new_password = serializers.CharField(max_length=Const.PASSWORD_MAX_LENGTH)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs.get('uid')).decode()
            self.user = models.User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            Error.invalid_uid()

        if not default_token_generator.check_token(
            self.user, attrs.get('token')
        ):
            Error.invalid_token()

        return attrs


class PasswordResetSerializer(Serializer):
    email = serializers.EmailField(max_length=Const.EMAIL_MAX_LENGTH)
    form_class = PasswordResetForm

    def validate(self, attrs):
        self.password_reset_form = self.form_class(data=self.initial_data)
        if not self.password_reset_form.is_valid():
            Error.required_field('email')

        self.language = Text.language()
        return attrs

    @async_func
    def save(self):
        if settings.DO_NOT_SEND_EMAIL:
            return

        users = models.User.objects.filter(
            username=self.validated_data.get('email')
        )
        if users.exists():
            user = users.latest('id')
        else:
            return

        Text.activate(self.language)

        opts = {
            'domain_override': settings.FRONTEND_URL,
            'subject_template_name': 'password_reset_subject.txt',
            'email_template_name': 'password_reset.html',
            'use_https': settings.EMAIL_USE_TLS,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': self.context.get('request'),
            'html_email_template_name': 'password_reset.html',
            'extra_email_context': {
                'site_name': settings.SITE_NAME,
                'call_name': user.call_name,
            },
        }
        self.password_reset_form.save(**opts)


class DeactivateAccountSerializer(Serializer):
    consent = serializers.BooleanField()

    def validate(self, attrs):
        if not attrs.get('consent'):
            Error.you_must_consent('consent')

        return attrs


class UserSettingSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'call_name',
            'photo',
            'tel',
            'address',
            'is_approved',
            'is_staff',
            'date_joined',
        ]
        read_only_fields = [
            'username',
            'is_approved',
            'is_staff',
            'date_joined',
        ]
        extra_kwargs = {
            'first_name': Const.NOT_NULL,
            'last_name': Const.NOT_NULL,
            'call_name': Const.NOT_NULL
        }


class IAmSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'call_name',
            'photo',
            'is_staff',
            'is_approved',
        ]


class UserIAMSerializer(Serializer):
    key = serializers.CharField()
    user = IAmSerializer()

    class Meta:
        fields = [
            'key',
            'user',
        ]


class LoginDeviceIAMSerializer(UserIAMSerializer):
    login_device = LoginDeviceSerializer()

    class Meta:
        fields = [
            'key',
            'user',
            'login_device',
        ]


class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'call_name',
            'photo',
            'tel',
            'address',
            'is_active',
            'is_approved',
            'date_joined',
            'last_login',
        ]


class StaffAdminSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'call_name',
            'photo',
            'tel',
            'address',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
            'last_login',
        ]


class UserIdSerializer(ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.approved(),
        required=False
    )

    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'call_name',
        ]
        read_only_fields = [
            'username',
            'call_name',
        ]


class UsernameSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'call_name',
        ]


class AuthCodeSerializer(ModelSerializer):
    class Meta:
        model = models.AuthCode
        fields = [
            'id',
            'email',
            'tel',
            'code',
            'wrong_input',
            'is_used',
            'created_at',
            'tried_at',
        ]


class SMSAuthSerializer(ModelSerializer):
    class Meta:
        model = models.AuthCode
        fields = [
            'id',
            'tel',
            'created_at',
        ]
        read_only_fields = [
            'created_at',
        ]
        extra_kwargs = {
            'tel': Const.REQUIRED,
        }


class EmailAuthSerializer(ModelSerializer):
    class Meta:
        model = models.AuthCode
        fields = [
            'id',
            'email',
            'created_at',
        ]
        read_only_fields = [
            'email',
            'created_at',
        ]


class AuthCodeAnswerSerializer(ModelSerializer):
    class Meta:
        model = models.AuthCode
        fields = [
            'email',
            'tel',
            'code',
        ]
        read_only_fields = [
            'email',
            'tel',
        ]
        extra_kwargs = {
            'code': {
                'required': True,
                'write_only': True,
                'allow_null': False,
                'allow_blank': False,
            }
        }
