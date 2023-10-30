from api.pagination import CommonPagination
from companies.models import Company
from django.contrib.auth import get_user_model
from django.http import FileResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from quizzes.models import AnswerOption, Question, Quiz, QuizResult, UsersAnswer
from quizzes.permissions import (
    DidUserCompletedTheSameQuiz,
    DoesUserAnswerExistAlready,
    IsAbleToCreateQuiz,
    IsAbleToEditAnswerOptionQuestion,
    IsAbleToEditDeleteQuiz,
    IsAbleToExportData,
    IsQuizResultScoreCalculated,
)
from quizzes.serializers import (
    AnswerOptionModelSerializer,
    QuestionModelSerializer,
    QuizModelSerializer,
    QuizResultModelSerializer,
    UsersAnswerModelSerializer,
)
from utils.caching import cache_user_answer
from utils.export_data import ExportDataFileType, export_quiz_result

User = get_user_model()

# Create your views here.
class QuizModelViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizModelSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CommonPagination

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsAbleToCreateQuiz, )
        elif self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = (IsAbleToEditDeleteQuiz, )
        return super().get_permissions()
    
    # Get list of company quizzes by id
    @action(detail=True, url_path='company_quizzes', methods=['get'])
    def get_company_quizzes_list(self, request, pk=None):
        queryset = Quiz.objects.filter(company_id=pk)

        if not queryset:
            return Response(
                {'detail': 'There are no quizzes from this company or the company does not exist'}, 
                status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionModelViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAbleToEditAnswerOptionQuestion, )
        return super().get_permissions()


class AnswerOptionModelViewSet(ModelViewSet):
    queryset = AnswerOption.objects.all()
    serializer_class = AnswerOptionModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAbleToEditAnswerOptionQuestion, )
        return super().get_permissions()

# Use mixins to unable DELETE methods in ModelViewSet
class QuizResultModelViewSet(GenericViewSet,
                             mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (DidUserCompletedTheSameQuiz, )
        elif self.action == 'partial_update':
            self.permission_classes = (IsQuizResultScoreCalculated, )
        return super().get_permissions()

    # Export data from Redis in CSV and JSON
    @action(detail=False, url_path='export_data', methods=['get'],
            permission_classes=[IsAbleToExportData])
    def export_quiz_result_data(self, request):
        user = None
        company = None
        file_type = request.query_params.get('file_type', ExportDataFileType.CSV.value)
        
        # Check if file_type param is valid
        if file_type != ExportDataFileType.CSV.value and file_type != ExportDataFileType.JSON.value:
            return Response({'detail': 'Wrong file_type parameter'}, status.HTTP_400_BAD_REQUEST)

        # Get data from query params
        user_id = request.query_params.get('user')
        company_id = request.query_params.get('company')

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response({'detail': 'User not found'}, status.HTTP_404_NOT_FOUND)
        
        if company_id:
            try:
                company = Company.objects.get(pk=company_id)
            except Company.DoesNotExist:
                return Response({'detail': 'Company not found'}, status.HTTP_404_NOT_FOUND)

        file_path = export_quiz_result(
            file_type=file_type, user_instance=user, company_instance=company
        )

        # Create a file response
        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True, 
            filename=f"redis_data.{file_type}"
        )

        return response

# Use mixins to unable PATCH, PUT, DELETE methods in ModelViewSet
class UsersAnswerModelViewSet(GenericViewSet,
                              mixins.RetrieveModelMixin,
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    queryset = UsersAnswer.objects.all()
    serializer_class = UsersAnswerModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (DoesUserAnswerExistAlready, )
        return super().get_permissions()
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            data = serializer.data

            quiz_company = Quiz.objects.get(pk=data['quiz']).company
            
            cache_user_answer(data, quiz_company.id)
            return Response(data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
