from rest_framework import permissions

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission based on user roles.
    """
    def has_permission(self, request, view):
        required_roles = getattr(view, 'required_roles', [])
        return request.user.is_authenticated and request.user.role.name in required_roles
