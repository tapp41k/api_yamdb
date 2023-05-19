from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """
    Даёт доступ только пользователям с ролью админа
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_admin
