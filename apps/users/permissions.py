from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to admins
        return request.user and request.user.is_staff

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission based on user roles
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Example role-based permission
        if view.action == 'create_room':
            return request.user.can_create_room()
        
        return True