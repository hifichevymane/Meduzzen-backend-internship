from companies.enums import CompanyMemberRole
from companies.models import Company, CompanyMembers
from rest_framework.permissions import BasePermission


class IsAbleToDeleteUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAbleToGetLastCompletionTime(BasePermission):
    def has_permission(self, request, view):
        company_id = view.kwargs.get('pk')
        user = request.user

        is_owner = Company.objects.filter(pk=company_id, owner=user).exists()
        is_admin = CompanyMembers.objects.filter(
            company_id=company_id, 
            user=user,
            role=CompanyMemberRole.ADMIN.value).exists()

        return is_admin or is_owner
