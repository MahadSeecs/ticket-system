from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    #allow only super admin to change user list
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == request.user.Role.SUPER_ADMIN
