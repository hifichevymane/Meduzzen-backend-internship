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
        user = request.user
        return not UsersAnswer.objects.filter(question_id=question_id, user=user).exists()


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
        quiz_result = QuizResult.objects.get(pk=pk)
        return quiz_result.status == UserQuizStatus.PENDING.value
