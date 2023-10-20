from companies.models import Company, CompanyMemberRole, CompanyMembers
from rest_framework.permissions import BasePermission

from quizzes.models import Quiz


class IsAbleToCreateQuiz(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            company_id = request.data.get('company')

            is_company_admin = CompanyMembers.objects.filter(
                company_id=company_id, 
                user=user, 
                role=CompanyMemberRole.ADMIN.value).exists()
            
            is_company_owner = Company.objects.filter(pk=company_id, owner=user).exists()

            return is_company_admin or is_company_owner
        else:
            return True


class IsAbleToEditDeleteQuiz(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['destroy', 'update', 'partial_update']:
            user = request.user
            quiz_id = view.kwargs.get('pk')

            try:
                quiz = Quiz.objects.get(pk=quiz_id)

                is_company_admin = CompanyMembers.objects.filter(
                    company=quiz.company, 
                    user=user, 
                    role=CompanyMemberRole.ADMIN.value).exists()
            
                is_company_owner = Company.objects.filter(pk=quiz.company.id, owner=user).exists()

                return is_company_admin or is_company_owner
            except Quiz.DoesNotExist:
                return False
        return False
