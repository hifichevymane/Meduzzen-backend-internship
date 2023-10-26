from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyModelViewSet)
router.register(r'company_invites', views.CompanyInvitationsModelViewSet)
router.register(r'company_members', views.CompanyMembersModelViewSet)
router.register(r'company_user_ratings', views.CompanyUserRatingModelViewSet)

urlpatterns = [
    path('', include(router.urls), name='companies')
]