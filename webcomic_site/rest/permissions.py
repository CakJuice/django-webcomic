from rest_framework import permissions


class OnlyAuthorCanUpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method != 'GET':
            return obj.author == request.user or request.user.is_superuser
        return True
