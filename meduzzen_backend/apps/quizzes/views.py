from api.pagination import CommonPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from quizzes.models import AnswerOption, Question, Quiz
from quizzes.permissions import IsAbleToCreateQuiz, IsAbleToEditAnswerOptionQuestion, IsAbleToEditDeleteQuiz
from quizzes.serializers import AnswerOptionModelSerializer, QuestionModelSerializer, QuizModelSerializer


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
