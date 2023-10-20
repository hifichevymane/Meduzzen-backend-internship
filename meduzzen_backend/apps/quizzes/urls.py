from django.urls import include, path
from rest_framework import routers

from quizzes import views

router = routers.SimpleRouter()
router.register(r'quizzes', views.QuizModelViewSet)
router.register(r'questions', views.QuestionModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
