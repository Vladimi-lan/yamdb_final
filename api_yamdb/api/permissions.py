from rest_framework import exceptions, permissions

from api_yamdb.settings import ME


class UserPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.parser_context['kwargs'].get('username') != ME:
            return bool(
                request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))
        if request.parser_context['kwargs'].get('username') == ME:
            if request.method == 'DELETE':
                raise exceptions.MethodNotAllowed(request.method)
        if request.method == 'DELETE':
            return bool(
                request.user.is_admin and request.user.is_superuser)
        return bool(request.user and request.user.is_authenticated)


class ReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class CreateAndUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_moderator
                or obj.author == request.user)


class IsModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_moderator
                or obj.author == request.user)


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.is_admin)
        )
