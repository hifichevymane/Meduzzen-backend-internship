from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyModelViewSet)
router.register(r'company_requests', views.CompanyRequestsModelViewSet)
router.register(r'company_members', views.CompanyMembersModelViewSet)
router.register(r'users_requests', views.UsersRequestsModelViewSet)

urlpatterns = [
    path('', include(router.urls), name='companies')
]