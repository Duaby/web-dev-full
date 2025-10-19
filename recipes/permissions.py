from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read permissions are allowed to any request.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff


class IsAuthenticatedOrPostOnly(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated users to POST,
    but require authentication for other methods.
    """
    def has_permission(self, request, view):
        # Allow POST requests from anyone
        if request.method == 'POST':
            return True
        
        # Require authentication for other methods
        return request.user and request.user.is_authenticated