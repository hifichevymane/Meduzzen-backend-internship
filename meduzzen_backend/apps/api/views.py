import logging

from companies.models import CompanyMembers
from companies.serializers import CompanyMembersReadModelSerializer
from django.contrib.auth import get_user_model
from quizzes.models import QuizResult
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAbleToDeleteUser
from .serializers import UserSerializer

User = get_user_model()

# Create a logger
test_logger = logging.getLogger('main')

# Create your views here.
# health_check endpoint
@api_view(['GET'])
def health_check(request):
    response = {'status_code': 200, 'detail': 'ok', 'result': 'working'}
    # Execute logger message
    test_logger.info('Test logging')
    return Response(response)


# User ViewSet to make CRUD operations. Use mixins to unable PUT PATCH request
class UserModelViewSet(GenericViewSet,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = (IsAbleToDeleteUser, )
        return super().get_permissions()

    # Ordering by 'created_at' field
    filter_backends = (OrderingFilter, )
    ordering = ('created_at', )

    # Calculate the avarage score of the current user in the entire system
    @action(detail=False, url_path='calculate_avarage_score', methods=['get'])
    def calculate_avarage_score(self, request):
        current_user = request.user
        user_obj = User.objects.get(pk=current_user.id)
        all_users_quiz_results = QuizResult.objects.filter(user=current_user)

        rating = 0
        all_correct_answers = 0 
        total_amount_questions = 0 # The amount of answered questions

        for result in all_users_quiz_results:
            all_correct_answers += result.score
            total_amount_questions += result.quiz.question_amount
        
        # Calculate the rating
        rating = all_correct_answers / total_amount_questions

        user_obj.rating = rating
        user_obj.save()

        serializer = self.serializer_class(user_obj)
        return Response({'rating': serializer.data['rating']}, status.HTTP_200_OK)

    # Get user's current company
    @action(detail=True, url_path='current_company', methods=['get'])
    def get_company_user_works_in(self, request, pk=None):
        try:
            queryset = CompanyMembers.objects.get(user_id=pk)

            serializer = CompanyMembersReadModelSerializer(queryset, context={'request': request})
            return Response(serializer.data)
        except CompanyMembers.DoesNotExist:
            return Response({'detail': 'Not found'}, status.HTTP_404_NOT_FOUND)
