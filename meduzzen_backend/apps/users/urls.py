from django.urls import include, path
from rest_framework import routers

from . import views

# Manage the endpoints for users model viewset
router = routers.SimpleRouter()
router.register(r'users_requests', views.UsersRequestsModelViewSet)

urlpatterns = [
    path('', include(router.urls), name='users'),
]
