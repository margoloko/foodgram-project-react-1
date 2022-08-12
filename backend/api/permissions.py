from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user and request.user.is_staff)


class AuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                request.user == obj.author or request.user.is_staff)


class AdminOrAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                request.user == obj.author or request.user.is_admin)
