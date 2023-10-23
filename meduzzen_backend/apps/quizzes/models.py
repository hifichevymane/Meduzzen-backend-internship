from api.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.
class Quiz(TimeStampedModel):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    frequency = models.IntegerField(default=0, blank=False, null=False)
    questions = models.ManyToManyField('Question', related_name='quizzes')

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
