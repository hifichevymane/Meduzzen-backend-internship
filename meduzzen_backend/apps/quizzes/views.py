from api.pagination import CommonPagination
from api.permissions import IsAbleToGetLastCompletionTime
from companies.models import Company
from django.contrib.auth import get_user_model
from django.db.models import Avg, FloatField, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from django.http import FileResponse
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from quizzes.enums import UserQuizStatus
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
    QuestionReadModelSerializer,
    QuestionWriteModelSerializer,
    QuizReadModelSerializer,
    QuizResultModelSerializer,
    QuizWriteModelSerializer,
    UsersAnswerModelSerializer,
)
from utils.analytics import set_start_end_date
from utils.caching import cache_user_answer
from utils.export_data import ExportDataFileType, export_quiz_result

User = get_user_model()

# Create your views here.
class QuizModelViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizWriteModelSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CommonPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return QuizReadModelSerializer
        return QuizWriteModelSerializer

    def get_permissions(self):
        permissions = super().get_permissions()

        if self.action == 'create':
            self.permission_classes = (IsAbleToCreateQuiz, )

        elif self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = (IsAbleToEditDeleteQuiz, )
        
        return permissions
    
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
        
    @action(detail=True, url_path='last_completions_time', 
            methods=['get'], permission_classes=(IsAbleToGetLastCompletionTime, ))
    def get_the_last_completions_time_of_quizzes(self, request, pk=None):
        last_result_subquery = QuizResult.objects.filter(
            quiz=OuterRef('pk')
        ).order_by('-updated_at').values('updated_at')[:1]

        # Get all quizzes' ids with the last completion time 
        queryset = Quiz.objects.filter(company_id=pk).annotate(
            last_taken_quiz_time=Subquery(last_result_subquery)
        ).values('id', 'last_taken_quiz_time')

        return Response(queryset)
    
    @action(detail=True, url_path='analytics', methods=['get'])
    def get_quiz_analytics(self, request, pk=None):
        # Get count of months from query_params
        months_count = request.query_params.get('months')

        # Get time interval
        time_interval = set_start_end_date(months_count)

        queryset = QuizResult.objects.filter(
            updated_at__range=time_interval,
            quiz_id=pk,
            status=UserQuizStatus.COMPLETED.value
        ).values('score')

        if not queryset:
            return Response({'detail': 'No quiz results were found'}, status.HTTP_404_NOT_FOUND)
        
        # Calculate avarage score
        avarage_score = 0
        for item in queryset:
            avarage_score += item['score']
        
        avarage_score /= len(queryset)

        return Response({'quiz': int(pk), 'avarage_score': round(avarage_score, 1)})

    @action(detail=True, url_path='selected_user_analytics', methods=['get'])
    def get_selected_user_analytics(self, request, pk=None):
        months_count = request.query_params.get('months')

        # Get time interval
        time_interval = set_start_end_date(months_count)

        avg_score_subquery = QuizResult.objects.filter(
            updated_at__range=time_interval,
            user_id=pk,
            status=UserQuizStatus.COMPLETED.value,
            quiz=OuterRef('id')
        ).values('quiz').annotate(
            avg_score=Coalesce(Avg('score'), Value(None))
        ).values('avg_score')[:1]

        queryset = Quiz.objects.all().values('id').annotate(
            avg_score=Coalesce(Subquery(avg_score_subquery), Value(0), output_field=FloatField())
        ).values('id', 'avg_score')

        return Response(queryset)


class QuestionModelViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionWriteModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return QuestionReadModelSerializer
        return QuestionWriteModelSerializer

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

        queryset = []
        data = []

        if user_id:
            user = User.objects.get(pk=user_id)
            if company_id: # Get the quiz results of a particular user in a company
                company = Company.objects.get(pk=company_id)
                queryset = QuizResult.objects.filter(user=user, company=company)
            else: # Get the quiz results of a particular user
                queryset = QuizResult.objects.filter(user=user)
        
        else:
            if company_id: # Get the quiz results of a particular company
                company = Company.objects.get(pk=company_id)
                queryset = QuizResult.objects.filter(company=company)
        
        # Generate data list
        if file_type == ExportDataFileType.CSV.value:
            for obj in queryset:
                record = (obj.id, obj.user, obj.company, obj.quiz, obj.score, obj.updated_at)
                data.append(record)
        else:
            for obj in queryset:
                record = {
                    'id': obj.id,
                    'user': obj.user.username,
                    'company': obj.company.name,
                    'quiz': obj.quiz.title,
                    'score': obj.score,
                    'date_passed': obj.updated_at
                }

                data.append(record)

        file_path = export_quiz_result(data, file_type=file_type)

        # Create a file response
        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True, 
            filename=f"exported_data.{file_type}"
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
