from rest_framework import permissions


class AdminOnlyPermission(permissions.BasePermission):
    def permission(self, request, view):
        if request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.is_admin:
            return True


class AuthorAdminModeratorObjectPermission(permissions.BasePermission):
    message = ('You have no rights for this action.')

    def permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.author == request.user:
            return True
        elif request.user.is_superuser:
            return True
        elif (request.user.is_authenticated
              and request.user.is_admin):
            return True
        elif (request.user.is_authenticated
              and request.user.is_moderator):
            return True


class AdminPermissionOrReadOnlyPermission(permissions.BasePermission):
    message = 'You have no rights for this action.'

    def permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        elif (request.user.is_authenticated
              and request.user.is_admin):
            return True


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated 
                and (request.user.is_superuser or request.user.role == 'Администратор'))



class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)