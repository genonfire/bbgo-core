from rest_framework import permissions as rest_permission


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


class IsSuperUser(rest_permission.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )
