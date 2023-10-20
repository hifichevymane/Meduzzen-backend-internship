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
    text = models.TextField(blank=False, null=False)
    options = models.JSONField(blank=False, null=False)
    answer = models.CharField(max_length=128, blank=False, null=False)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    def __str__(self) -> str:
        return self.text
