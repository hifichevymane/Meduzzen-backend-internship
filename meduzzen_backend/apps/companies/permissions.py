from rest_framework.permissions import BasePermission


# Is staff permission
class IsStaff(BasePermission):
    edit_methods = ('PUT', 'PATCH')

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Limit staff responsibilities to update records
        return request.user.is_staff and request.method not in self.edit_methods

# Is super user permission
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

# Is user owner permission
class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    # If user is owner of the company
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
