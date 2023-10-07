from django.urls import path

from . import views

urlpatterns = [
    path('companies/', views.CompanyListAPIView.as_view(), name='companies_list'),
    path('companies/', views.CompanyCreateAPIView.as_view(), name='companies_create'),
    path('companies/<int:pk>/', views.CompanyRetrieveUpdateDestroyAPIView.as_view(),
          name='companies_detail_update_delete')
]