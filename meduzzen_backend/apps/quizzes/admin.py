from django.contrib import admin

from quizzes.models import AnswerOption, Question, Quiz


class QuizAdmin(admin.ModelAdmin):
    search_fields = ('company', 'title', 'description')
    list_filter = ('company', 'frequency', 'questions')


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_filter = ('text', )


class AnswerOptionAdmin(admin.ModelAdmin):
    search_fields = ('text', 'creator')
    list_filter = ('text', 'creator')


# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)
