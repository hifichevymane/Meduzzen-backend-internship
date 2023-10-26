from django.urls import include, path
from rest_framework import routers

from quizzes import views

router = routers.SimpleRouter()
router.register(r'quizzes', views.QuizModelViewSet)
router.register(r'questions', views.QuestionModelViewSet)
router.register(r'answer_options', views.AnswerOptionModelViewSet)
router.register(r'quiz_results', views.QuizResultModelViewSet)
router.register(r'users_answers', views.UsersAnswerModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
