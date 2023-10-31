from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from companies.enums import CompanyInvitationStatus, CompanyMemberRole
from companies.models import Company, CompanyInvitations, CompanyMembers

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


class IsUserNotCompanyMember(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.data.get('user')
            if not user: # Get user from request.user
                user = request.user

            company = request.data.get('company')
            return not CompanyMembers.objects.filter(company=company, user=user).exists()
        return False


# Check if Owner has already sent invite
class HasOwnerNotSentInviteYet(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            company = request.data.get('company')
            user = request.data.get('user')
            # Return true if owner has not already sent invite
            return not CompanyInvitations.objects.filter(
                company=company, user=user, 
                status=CompanyInvitationStatus.PENDING.value
            ).exists()
        return False


class DoesOwnerSendInviteToItself(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            owner = request.user
            user = request.data.get('user')
            return owner.id != user
        return False


class IsAbleToDeleteCompanyUserRating(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return CompanyMembers.objects.filter(user=user, role=CompanyMemberRole.ADMIN.value).exists()
