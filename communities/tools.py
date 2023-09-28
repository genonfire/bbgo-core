from django.utils import timezone

from core.permissions import (
    AllowAny,
    DenyAll,
    IsAdminUser,
    IsApproved,
)
from utils.constants import Const
from utils.debug import Debug  # noqa


def delete_thread(instance):
    instance.is_pinned = False
    instance.is_deleted = True
    instance.modified_at = timezone.now()
    instance.save(update_fields=['is_deleted', 'is_pinned', 'modified_at'])


def restore_thread(instance):
    instance.is_deleted = False
    instance.modified_at = timezone.now()
    instance.save(update_fields=['is_deleted', 'modified_at'])


def pin_thread(instance):
    instance.is_pinned = True
    instance.save(update_fields=['is_pinned'])


def unpin_thread(instance):
    instance.is_pinned = False
    instance.save(update_fields=['is_pinned'])


def delete_reply(instance):
    instance.is_deleted = True
    instance.modified_at = timezone.now()
    instance.save(update_fields=['is_deleted', 'modified_at'])


def permission(forum, action):
    if action == Const.P_READ:
        perm = forum.option.get('permission_read')
    elif action == Const.P_WRITE:
        perm = forum.option.get('permission_write')
    elif action == Const.P_REPLY:
        perm = forum.option.get('permission_reply')
    else:
        raise AttributeError(
            "unknown action(%s) for forum(%s)" % (action, forum)
        )

    if perm == Const.PERMISSION_ALL:
        return [AllowAny]
    elif perm == Const.PERMISSION_MEMBER:
        return [IsApproved]
    elif perm == Const.PERMISSION_STAFF:
        return [IsAdminUser]
    else:
        raise AttributeError(
            "unknown permission(%s) for forum(%s)" % (perm, forum)
        )


def read_permission(forum):
    if not forum.is_active:
        return [IsAdminUser]

    return permission(forum, Const.P_READ)


def write_permission(forum):
    if not forum.is_active:
        return [DenyAll]

    return permission(forum, Const.P_WRITE)


def reply_permission(forum):
    if not forum.is_active:
        return [DenyAll]

    return permission(forum, Const.P_REPLY)


def date_or_time(in_time):
    today = timezone.localtime()
    created_at = timezone.localtime(in_time)

    if created_at.date() == today.date():
        return {
            'date': None,
            'time': created_at.time().strftime(Const.TIME_FORMAT_DEFAULT),
        }
    else:
        return {
            'date': created_at.date(),
            'time': None,
        }
