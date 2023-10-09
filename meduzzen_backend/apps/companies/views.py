from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from companies.models import Company
from companies.permissions import IsOwner, IsStaff, IsSuperUser

from .serializers import CompanyCreateSerializer, CompanyDetailSerializer


# Pagination class for CompanyModelViewSet
class CompanyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your views here.
# Company Model ViewSet
class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CompanyPagination

    # If action is create -> we use CompanyCreateSerializer
    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyCreateSerializer

        return super(CompanyModelViewSet, self).get_serializer_class()
    
    # Assign custom permission classes for PUT PATCH DELETE requests
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSuperUser | IsOwner | IsStaff ]
        return super().get_permissions()

    # Override list method to list only visible companies
    def list(self, request, *args, **kwargs):
        queryset = Company.objects.filter(visibility='visible')
        page = self.paginate_queryset(queryset) # Paginate queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
