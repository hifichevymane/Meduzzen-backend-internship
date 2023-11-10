from companies.models import Company, CompanyMemberRole, CompanyMembers
from rest_framework.permissions import BasePermission

from quizzes.models import Quiz, QuizResult, UserQuizStatus, UsersAnswer


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


class IsAbleToEditAnswerOptionQuestion(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class DoesUserAnswerExistAlready(BasePermission):
    def has_permission(self, request, view):
        question_id = request.data.get('question')
        quiz_result_id = request.data.get('quiz_result_id')
        user = request.user
        return not UsersAnswer.objects.filter(
            question_id=question_id, user=user,
            quiz_result_id=quiz_result_id
        ).exists()


# Check if user has already the same quiz with pending status(he is still undergoing it)
class DidUserCompletedTheSameQuiz(BasePermission):
    def has_permission(self, request, view):
        quiz_id = request.data.get('quiz')
        user = request.user
        return not QuizResult.objects.filter(
            quiz_id=quiz_id, 
            user=user, 
            status=UserQuizStatus.PENDING.value).exists()


class IsQuizResultScoreCalculated(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        is_quiz_result_calculated = QuizResult.objects.filter(
            pk=pk, status=UserQuizStatus.PENDING.value).exists()
        
        return is_quiz_result_calculated


class IsAbleToExportData(BasePermission):
    def has_permission(self, request, view):
        current_user = request.user
        passed_user_id = request.query_params.get('user')
        passed_company_id = request.query_params.get('company')

        is_current_user = False
        is_owner = False
        is_company_admin = False

        if passed_company_id:
            is_owner = Company.objects.filter(pk=passed_company_id, owner=current_user).exists()

            if passed_user_id:
                is_company_admin = CompanyMembers.objects.filter(
                    user=current_user, 
                    company_id=int(passed_company_id),
                    role=CompanyMemberRole.ADMIN.value
                    ).exists()

        if passed_user_id:
            is_current_user = current_user.id == int(passed_user_id)

        return is_current_user or is_owner or is_company_admin
