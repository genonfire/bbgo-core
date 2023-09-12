from django.utils import timezone

from core.permissions import (
    AllowAny,
    DenyAll,
    IsAdminUser,
    IsApproved,
)
from utils.constants import Const
from utils.debug import Debug  # noqa


def destroy_forum(instance):
    instance.option.delete()
    instance.delete()


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
        perm = forum.option.permission_read
    elif action == Const.P_WRITE:
        perm = forum.option.permission_write
    elif action == Const.P_REPLY:
        perm = forum.option.permission_reply
    else:
        raise AttributeError(
            "unknown action(%s) for forum(%s)" % (action, forum)
        )

    if perm == 'all':
        return [AllowAny]
    elif perm == 'member':
        return [IsApproved]
    elif perm == 'staff':
        return [IsAdminUser]
    else:
        raise AttributeError(
            "unknown permission(%s) for forum(%s)" % (perm, forum)
        )


def read_permission(forum):
    if not forum.option.is_active:
        return [IsAdminUser]

    return permission(forum, Const.P_READ)


def write_permission(forum):
    if not forum.option.is_active:
        return [DenyAll]

    return permission(forum, Const.P_WRITE)


def reply_permission(forum):
    if not forum.option.is_active:
        return [DenyAll]

    return permission(forum, Const.P_REPLY)
