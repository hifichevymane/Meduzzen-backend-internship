from datetime import datetime

from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

from .enums import UserQuizStatus

User = get_user_model()

# Create your models here.
class QuizResult(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    score = models.IntegerField(default=0, blank=False, null=False)
    # Status of passing quiz
    status = models.CharField(
        default=UserQuizStatus.PENDING.value,
        choices=UserQuizStatus.choices(),
        blank=False, null=False)
    
    @staticmethod
    def get_all_users_analytics(start_date: datetime, end_date: datetime):
        avg_scores_subquery = QuizResult.objects.filter(
            user=models.OuterRef('id'),
            updated_at__range=(start_date, end_date),
            status=UserQuizStatus.COMPLETED.value
        ).values('user').annotate(
            average_score=models.Avg('score')
        ).values('average_score')[:1]

        return User.objects.annotate(
            average_score=models.Subquery(avg_scores_subquery)
        ).values('id', 'average_score')

    class Meta:
        verbose_name = 'Quiz result'
        verbose_name_plural = 'Quiz results'

    def __str__(self) -> str:
        return f'{self.quiz} - {self.user} - {self.score} score'


class Quiz(TimeStampedModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    frequency = models.IntegerField(default=0, blank=False, null=False)
    questions = models.ManyToManyField('Question', related_name='quizzes', blank=True)
    question_amount = models.IntegerField(blank=False, null=False)

    # Get the average score of a quiz across entire system
    @property
    def rating(self):
        return QuizResult.objects.filter(
            quiz=self,
            status=UserQuizStatus.COMPLETED.value
        ).aggregate(rating=models.Avg('score'))['rating']
    
    @staticmethod
    def get_last_completions_time_of_quizzes(company_id: models.ForeignKey):
        last_result_subquery = QuizResult.objects.filter(
            quiz=models.OuterRef('pk')
        ).order_by('-updated_at').values('updated_at')[:1]

        # Get all quizzes' ids with the last completion time 
        queryset = Quiz.objects.filter(company_id=company_id).annotate(
            last_taken_quiz_time=models.Subquery(last_result_subquery)
        ).values('id', 'last_taken_quiz_time')

        return queryset
    
    @staticmethod
    def get_all_quizzes_analytics(start_date: datetime, end_date: datetime):
        return Quiz.objects.filter(
            quizresult__updated_at__range=(start_date, end_date),
            quizresult__status=UserQuizStatus.COMPLETED.value
        ).annotate(
            average_score=models.Avg('quizresult__score')
        ).values('id', 'average_score')
    
    @staticmethod
    def get_selected_user_analytics(user_id: models.ForeignKey ,start_date: datetime, end_date: datetime):
        avg_score_subquery = QuizResult.objects.filter(
            updated_at__range=(start_date, end_date),
            user_id=user_id,
            status=UserQuizStatus.COMPLETED.value,
            quiz=models.OuterRef('id')
        ).values('quiz').annotate(
            average_score=models.Avg('score')
        ).values('average_score')[:1]

        return Quiz.objects.all().values('id').annotate(
            average_score=models.Subquery(avg_score_subquery)
        ).values('id', 'average_score')

    def get_quiz_analytics(self, start_date: datetime, end_date: datetime) -> dict[str: float]:
        return Quiz.objects.filter(
            quizresult__updated_at__range=(start_date, end_date),
            quizresult__status=UserQuizStatus.COMPLETED.value,
            id=self.id
        ).aggregate(average_score=models.Avg('quizresult__score'))

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'

    def __str__(self) -> str:
        return self.title


class Question(TimeStampedModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)
    options = models.ManyToManyField('AnswerOption', related_name='options')
    answer = models.ManyToManyField('AnswerOption', related_name='answers')

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return self.text


class AnswerOption(TimeStampedModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'Answer option'
        verbose_name_plural = 'Answer options'

    def __str__(self) -> str:
        return self.text


# Users' answers on quizzes questions
class UsersAnswer(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Ability to select multiple answer options
    answer = models.ManyToManyField(AnswerOption, related_name='user_answers')
    is_correct = models.BooleanField(blank=False, null=False)
    # If user wants to undergo the same quiz multiple times
    quiz_result = models.ForeignKey(QuizResult, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Users answer'
        verbose_name_plural = 'Users answers'
