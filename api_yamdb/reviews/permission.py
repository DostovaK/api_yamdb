from rest_framework import permissions


class AuthorAdminModeratorObjectPermission(permissions.BasePermission):
    message = ('You have no rights for this action.')

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.author == request.user:
            return True
        elif request.user.is_superuser:
            return True
        elif (
                request.user.is_authenticated
                and request.user.is_admin):
            return True
        elif (
                request.user.is_authenticated
                and request.user.is_moderator
        ):
            return True
