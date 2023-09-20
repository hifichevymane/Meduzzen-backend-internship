from django.urls import path
from . import views

urlpatterns = [
    # health_check endpoint url
    path('', views.health_check, name='health_check'),
]
