from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """Allows access only to users who are clients."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'client'

class IsArtisan(BasePermission):
    """Allows access only to users who are artisans."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'artisan'

class IsOwner(BasePermission):
    """Allows users to edit their own profile but not others'."""
    def has_object_permission(self, request, view, obj):
        return obj == request.user
