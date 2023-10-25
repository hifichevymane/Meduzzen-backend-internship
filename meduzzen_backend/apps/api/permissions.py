from rest_framework.permissions import BasePermission


class IsAbleToDeleteUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user
