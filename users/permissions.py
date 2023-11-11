from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


class IsSeller(BasePermission):
    message = "Access Denied!"

    def has_permission(self, request, view):
        if not request.user.is_anonymous and request.user.role == User.Role.SELLER:
            return True
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
