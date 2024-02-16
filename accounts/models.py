from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager
)
from django.db import models
from django.db.models import Q
from django.utils import timezone

from core.fields import EncryptedCharField
from utils.constants import Const
from utils.datautils import true_or_false
from utils.debug import Debug  # noqa

from . import tools


class UserManager(DjangoUserManager):
    def active(self):
        return self.filter(is_superuser=False).filter(is_active=True)

    def approved(self):
        return self.active().filter(is_approved=True)

    def staff(self):
        return self.approved().filter(is_staff=True)

    def query_active(self, q):
        active = true_or_false(q.get(Const.QUERY_PARAM_ACTIVE))
        if active:
            return Q(is_active=active)
        else:
            return Q()

    def query_staff(self, q):
        return Q(is_staff=True) & self.query_active(q)

    def query_anti_staff(self, q):
        return Q(is_staff=False) & self.query_active(q)

    def user_query(self, q):
        search_query = Q()
        if q:
            search_query = (
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q) |
                Q(call_name__icontains=q)
            )
        return search_query

    def search(self, q, filters):
        if not filters:
            filters = Q()

        return self.filter(filters).filter(self.user_query(q)).distinct()


class User(AbstractUser):
    username = models.EmailField(
        unique=True,
    )
    first_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    call_name = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to='photo/',
        max_length=Const.FILE_MAX_LENGTH,
        blank=True,
        null=True,
    )
    tel = EncryptedCharField(
        max_length=Const.TEL_MAX_LENGTH,
        blank=True,
        null=True,
    )
    address = EncryptedCharField(
        max_length=Const.ADDRESS_MAX_LENGTH,
        blank=True,
        null=True
    )
    is_approved = models.BooleanField(default=False)

    objects = UserManager()

    EMAIL_FIELD = 'username'

    class Meta:
        ordering = ['-id']

    def token(self):
        return tools.get_auth_token(self)

    def key(self):
        return self.token().key


class LoginDeviceManager(models.Manager):
    pass


class LoginDevice(models.Model):
    user = models.ForeignKey(
        'User',
        related_name='device_user',
        on_delete=models.CASCADE,
        null=True,
    )
    device = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    os = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    browser = models.CharField(
        max_length=Const.NAME_MAX_LENGTH,
        blank=True,
        null=True,
    )
    ip_address = models.CharField(
        max_length=Const.IP_ADDRESS_MAX_LENGTH,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)

    objects = LoginDeviceManager()

    class Meta:
        ordering = ['-id']


class AuthCodeManager(models.Manager):
    def search(self, q=None, used=None, success=None):
        if q:
            search_query = (
                Q(email__icontains=q) |
                Q(tel__icontains=q)
            )
        else:
            search_query = Q()

        if used:
            used_query = Q(is_used=used)
        else:
            used_query = Q()

        if success:
            success_query = (
                Q(is_used=True) &
                Q(wrong_input__isnull=bool(success == 'True'))
            )
        else:
            success_query = Q()

        return self.filter(
            search_query
        ).filter(used_query).filter(success_query)


class AuthCode(models.Model):
    email = models.EmailField(
        blank=True,
        null=True,
    )
    tel = models.CharField(
        max_length=Const.TEL_MAX_LENGTH,
        blank=True,
        null=True,
    )
    code = models.CharField(
        max_length=Const.AUTH_CODE_LENGTH,
        blank=True,
        null=True,
    )
    wrong_input = models.CharField(
        max_length=Const.AUTH_CODE_LENGTH,
        blank=True,
        null=True,
    )
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(default=timezone.now)

    objects = AuthCodeManager()

    class Meta:
        ordering = ['-id']

    def expired_at(self):
        return (
            timezone.localtime(self.created_at) +
            timezone.timedelta(seconds=Const.AUTH_CODE_EXPIRATION_SECONDS)
        )

    def tried_at(self):
        if self.is_used:
            return self.used_at
        else:
            return None
