from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin)))

# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS
#                 or (request.user.is_authenticated and (
#                     request.user.is_admin or request.user.is_superuser)))


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminRole(BasePermission):
    """
    Даёт доступ только пользователям с ролью админа
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin
