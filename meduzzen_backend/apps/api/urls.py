from django.urls import include, path
from rest_framework import routers

from . import views

# Manage the endpoints for users model viewset
router = routers.SimpleRouter()
router.register(r'users', views.UserModelViewSet)

urlpatterns = [
    # health_check endpoint url
    path('', views.health_check, name='health_check'),
    path('', include(router.urls), name='users'),
    path('', include('companies.urls'), name='companies'),
    # Djoser auth pathes
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Djoser social auth paths
    path('auth/', include('djoser.social.urls')),
]
