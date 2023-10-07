from rest_framework.permissions import BasePermission


# Is staff permission
class IsStaff(BasePermission):
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Limit staff responsibilities to update records
        if request.user.is_staff and request.method not in self.edit_methods:
            return True
        return False

# Is super user permission
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False

# Is user owner permission
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    # If user is owner of the company
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
