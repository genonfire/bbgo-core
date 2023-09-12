import random

from user_agents import parse

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.crypto import get_random_string

from rest_framework.authtoken.models import Token

from utils.constants import Const
from utils.text import Text
from utils.debug import Debug  # noqa


class _Test:
    USERNAME = '1@a.com'
    PASSWORD = 'password'
    FIRST_NAME = 'B'
    LAST_NAME = 'B'
    CALL_NAME = 'B B'
    KEY = 'e6e02990878c735f790f251561788bf44f15e7ed'


Test = _Test()


def get_call_name(first_name, last_name, language=None):
    if not language:
        language = Text.language()

    if language in Const.LANG_SURNAME_AHEAD:
        call_name = '%s %s' % (last_name, first_name)
    else:
        call_name = '%s %s' % (first_name, last_name)

    return call_name


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_user_agent(request):
    ua_string = request.META.get('HTTP_USER_AGENT')
    if ua_string:
        user_agent = parse(request.META.get('HTTP_USER_AGENT'))
        browser = user_agent.browser
        os = user_agent.os
        device = user_agent.is_pc and 'PC' or user_agent.device.family

        return device, os.family, browser.family
    else:
        return 'Other', 'Other', 'Other'


def is_same_device(request, login_device):
    ip_address = get_ip_address(request)
    device, os, browser = get_user_agent(request)

    if (
        request.user == login_device.user and
        ip_address == login_device.ip_address and
        device == login_device.device and
        os == login_device.os and
        browser == login_device.browser
    ):
        return True
    else:
        return False


def register_device(login_device):
    login_device.is_registered = True
    login_device.save(update_fields=['is_registered'])


def delete_device(login_device):
    if login_device:
        login_device.delete()


def set_last_login(device=None, user=None):
    now = timezone.now()

    if device:
        device.last_login = now
        device.save(update_fields=['last_login'])

        if not user:
            user = device.user

    if user:
        user.last_login = now
        user.save(update_fields=['last_login'])


def get_auth_token(user):
    if (Debug.debug_or_test_mode() and
            user.username == Test.USERNAME and
            not Token.objects.filter(user=user).exists()):
        # Use for test only: for postman collections
        token = Token.objects.create(
            key=Test.KEY,
            user=user
        )
    else:
        token, _ = Token.objects.get_or_create(user=user)

    return token


def approve_user(user, auth_code):
    if auth_code.tel:
        user.tel = auth_code.tel
        user.is_approved = True
    elif auth_code.email:
        user.is_approved = True
    else:
        Debug.error('Wrong auth type for %s' % auth_code)
    user.save()


def delete_auth_token(user):
    try:
        user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        return False
    return True


def generate_auth_code(digit=0):
    if digit == 0:
        digit = Const.AUTH_CODE_LENGTH

    code = ''
    for _ in range(digit):
        code += '%s' % random.randint(0, 9)
    return code


def destory_authcode(user, authcode_model):
    authcode_model.objects.filter(email=user.username).delete()
    if user.tel:
        authcode_model.objects.filter(tel=user.tel).delete()


def get_censored_username(prefix):
    return prefix + get_random_string(9) + Const.CENSORED_EMAIL_DOMAIN


def destroy_privacy(user):
    user.first_name = None
    user.last_name = None
    user.call_name = None
    user.tel = None
    user.address = None
    if user.photo:
        user.photo.delete()

    user.username = get_censored_username(user.username[0])
    user.email = user.username


def deactivate_account(user, authcode_model):
    Debug.trace('Deactivating %s' % user)

    if authcode_model:
        destory_authcode(user, authcode_model)
    destroy_privacy(user)

    user.is_superuser = False
    user.is_staff = False
    user.is_active = False
    user.is_approved = False
    user.last_login = timezone.now()

    user.save()
    user.token().delete()
