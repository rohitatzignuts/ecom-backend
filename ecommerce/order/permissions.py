from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, obj, view):
        # Check if the object's owner matches the current user
        return obj.owner == request.user
