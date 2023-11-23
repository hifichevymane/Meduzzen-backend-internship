import logging

from companies.models import CompanyMembers
from companies.serializers import CompanyMembersReadModelSerializer
from django.contrib.auth import get_user_model
from quizzes.models import Quiz, QuizResult
from quizzes.serializers import QuizLastCompletionTimeSerializer
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.serializers import AnalyticsSerializer

from .permissions import IsAbleToDeleteUpdateUser
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
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action in ['destroy', 'partial_update', 'update']:
            self.permission_classes = (IsAbleToDeleteUpdateUser, )
        return super().get_permissions()

    # Ordering by 'created_at' field
    filter_backends = (OrderingFilter, )
    ordering = ('created_at', )

    # Calculate the avarage score of the current user in the entire system
    @action(detail=False, url_path='calculate_avarage_score', methods=['get'])
    def calculate_avarage_score(self, request):
        current_user = request.user
        rating = QuizResult.calculate_user_rating(user=current_user)

        if not rating:
            return Response({'detail': 'You have not completed any quizzes'}, status.HTTP_404_NOT_FOUND)
        return Response(rating)

    # Get user's current company
    @action(detail=True, url_path='current_company', methods=['get'])
    def get_company_user_works_in(self, request, pk=None):
        queryset = CompanyMembers.get_company_user_works_in(user_id=pk)

        if queryset:
            serializer = CompanyMembersReadModelSerializer(queryset, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not found'}, status.HTTP_404_NOT_FOUND)
    
    # Get list of average scores of all users with dynamics over time
    @action(detail=False, url_path='analytics', methods=['post'])
    def users_analytics(self, request): 
        serializer = AnalyticsSerializer(data=request.data)

        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            queryset = QuizResult.get_all_users_analytics(start_date, end_date)
            return Response(queryset)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, url_path='last_quizzes_completion_times', methods=['get'])
    def get_user_last_quizzes_completion_times(self, request, pk=None):
        company_user_works_in = CompanyMembers.get_company_user_works_in(user_id=pk).last()

        if company_user_works_in:
            queryset = Quiz.get_last_completions_time_of_quizzes(
                user_id=pk, 
                company_id=company_user_works_in.company.id
            )
            serializer = QuizLastCompletionTimeSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'detail': 'Not found'}, status.HTTP_404_NOT_FOUND)
