from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

from applications.users.choices import UserRole


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return request.user == obj.owner or request.user.role == UserRole.ADMIN.name

