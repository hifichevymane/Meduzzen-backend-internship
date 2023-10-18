from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from companies.models import Company

User = get_user_model()

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
    
# Is the owner of company the current user
class IsUsersCompany(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy', 'update', 'partial_update']:
            company_id = request.data.get('company')
            if company_id is not None:
                try:
                    company = Company.objects.get(id=company_id)
                    return company.owner == request.user
                except Company.DoesNotExist:
                    return False
                
        elif view.action:
            company_id = view.kwargs.get('pk')
            if company_id is not None:
                try:
                    company = Company.objects.get(id=company_id)
                    return company.owner == request.user
                except Company.DoesNotExist:
                    return False

        return True
    
    def has_object_permission(self, request, view, obj):        
        return obj.company.owner == request.user


class IsInvitedUser(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'destroy', 'update', 'partial_update']:
            user_id = request.data.get('user')
            if user_id is not None:
                try:
                    return user_id == request.user.id
                except User.DoesNotExist:
                    return False  
        return True  
    
    def has_object_permission(self, request, view, obj):        
        return obj.user == request.user
