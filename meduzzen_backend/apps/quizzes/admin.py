from django.contrib import admin

from quizzes.models import AnswerOption, Question, Quiz, QuizResult, UsersAnswer


class QuizAdmin(admin.ModelAdmin):
    search_fields = ('company', 'title', 'description', 'creator')
    list_filter = ('company', 'questions', 'creator')
    list_display = ('title', 'creator', 'company', 'pk')


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ('text', )
    list_filter = ('text', )
    list_display = ('text', 'pk')


class AnswerOptionAdmin(admin.ModelAdmin):
    search_fields = ('text', 'creator')
    list_filter = ('text', 'creator')
    list_display = ('text', 'creator', 'pk')


class QuizResultAdmin(admin.ModelAdmin):
    search_fields = ('user', 'quiz', 'company', 'status')
    list_filter = ('user', 'quiz', 'company', 'status')
    list_display = ('user', 'quiz', 'company', 'status', 'pk')


class UsersAnswerAdmin(admin.ModelAdmin):
    search_fields = ('user', 'quiz', 'question', 'answer')
    list_filter = ('user', 'quiz', 'question', 'answer')
    list_display = ('quiz_result', 'question', 'is_correct', 'quiz', 'user', 'pk')

# Register your models here.
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(AnswerOption, AnswerOptionAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(UsersAnswer, UsersAnswerAdmin)
