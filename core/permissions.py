from rest_framework import permissions as rest_permission

from utils.constants import Const


class AllowAny(rest_permission.AllowAny):
    pass


class DenyAll(rest_permission.BasePermission):
    def has_permission(self, request, view):
        return False


class IsAuthenticated(rest_permission.IsAuthenticated):
    pass


class IsAuthenticatedOrReadOnly(rest_permission.IsAuthenticatedOrReadOnly):
    pass


class IsApproved(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_approved
        )


class IsApprovedOrReadOnly(rest_permission.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in rest_permission.SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_approved
        )


class IsAdminUser(rest_permission.IsAdminUser):
    pass


class IsAdminOrReadOnly(rest_permission.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in rest_permission.SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


class IsSuperUser(rest_permission.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )


class _ContentPermission():
    P_LIST = 'list'
    P_READ = 'read'
    P_WRITE = 'write'
    P_REPLY = 'reply'
    P_VOTE = 'vote'

    def permission(self, obj, action):
        if action == self.P_LIST:
            perm = obj.option.get('permission_list')
        elif action == self.P_READ:
            perm = obj.option.get('permission_read')
        elif action == self.P_WRITE:
            perm = obj.option.get('permission_write')
        elif action == self.P_REPLY:
            perm = obj.option.get('permission_reply')
        elif action == self.P_VOTE:
            perm = obj.option.get('permission_vote')
        else:
            raise AttributeError(
                "unknown action(%s) for obj(%s)" % (action, obj)
            )

        if perm == Const.PERMISSION_ALL:
            return [AllowAny]
        elif perm == Const.PERMISSION_MEMBER:
            return [IsApproved]
        elif perm == Const.PERMISSION_STAFF:
            return [IsAdminUser]
        else:
            raise AttributeError(
                "unknown permission(%s) for obj(%s)" % (perm, obj)
            )

    def list(self, obj):
        return self.permission(obj, self.P_LIST)

    def read(self, obj):
        return self.permission(obj, self.P_READ)

    def write(self, obj):
        return self.permission(obj, self.P_WRITE)

    def reply(self, obj):
        return self.permission(obj, self.P_REPLY)

    def vote(self, obj):
        return self.permission(obj, self.P_VOTE)


class _ForumPermission(_ContentPermission):
    def list(self, obj):
        if not obj.is_active:
            return [IsAdminUser]

        return self.permission(obj, self.P_LIST)

    def read(self, obj):
        if not obj.is_active:
            return [IsAdminUser]

        return self.permission(obj, self.P_READ)

    def write(self, obj):
        if not obj.is_active:
            return [DenyAll]

        return self.permission(obj, self.P_WRITE)

    def reply(self, obj):
        if not obj.is_active:
            return [DenyAll]

        return self.permission(obj, self.P_REPLY)

    def vote(self, obj):
        if not obj.is_active:
            return [DenyAll]

        return self.permission(obj, self.P_VOTE)


ContentPermission = _ContentPermission()
ForumPermission = _ForumPermission()
