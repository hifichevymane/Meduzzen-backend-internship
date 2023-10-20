from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'users', views.UserModelViewSet)

urlpatterns = [
    # health_check endpoint url
    path('', views.health_check, name='health_check'),
    path('', include('companies.urls'), name='companies'),
    path('', include('users.urls'), name='users'),
    path('', include(router.urls)),
    # Djoser auth pathes
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    # Djoser social auth paths
    path('auth/', include('djoser.social.urls')),
]
