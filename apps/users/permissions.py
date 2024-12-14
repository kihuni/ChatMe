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
        return request.user and request.user.is_staff and request.user.is_active

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission based on user roles
    """
ROLE_PERMISSIONS = {
    'create_room': ['admin', 'moderator'],
    'delete_room': ['admin'],
}

def has_permission(self, request, view):
    if not request.user.is_authenticated:
        return False
    
    # Get the required roles for this action
    required_roles = self.ROLE_PERMISSIONS.get(view.action, [])
    
    # Allow if the user's role matches any of the required roles
    return request.user.role and request.user.role.name in required_roles
