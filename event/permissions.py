from rest_framework import permissions


class UpdateOwnObjects(permissions.BasePermission):
    """allowing to update own profile"""

    def has_object_permission(self, request, view, obj):
        """checking the request id is equal to obj id"""
        return request.user.id == obj.provider.id