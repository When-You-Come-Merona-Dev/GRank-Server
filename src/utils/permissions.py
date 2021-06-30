from fastapi import Request
from src.utils.exceptions import PermissionDeniedException


def get_permissions(permissions):
    return [permission() for permission in permissions]


def check_permissions(request: Request, permissions) -> None:
    for permission in get_permissions(permissions):
        if not permission.has_permission(request):
            permission.permission_denied()
    return


class BasePermission:
    exception = PermissionDeniedException

    def has_permission(self, request):
        return True

    def has_object_permission(self, request, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def permission_denied(self):
        raise self.exception()


class AllowAny(BasePermission):
    exception = PermissionDeniedException

    def has_permission(self, request):
        return True


class IsAuthenticated(BasePermission):
    exception = PermissionDeniedException

    def has_permission(self, request):
        if getattr(request.user, "is_authenticated", False):
            return True
        return False
