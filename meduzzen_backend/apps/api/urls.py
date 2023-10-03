from django.urls import path, include
from rest_framework import routers
from . import views

# Manage the endpoints for users model viewset
# https://www.django-rest-framework.org/api-guide/routers/
router = routers.SimpleRouter()
router.register(r'users', views.UserModelViewSet)

urlpatterns = [
    # health_check endpoint url
    path('', views.health_check, name='health_check'),
    path('', include(router.urls))
]
