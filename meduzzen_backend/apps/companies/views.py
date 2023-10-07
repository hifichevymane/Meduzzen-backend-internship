from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.permissions import IsOwner, IsStaff, IsSuperUser

from .serializers import CompanyCreateSerializer, CompanyDetailSerializer


# Create your views here.
# List of all companies
class CompanyListAPIView(ListAPIView):
    # Get only visible companies
    queryset = Company.objects.filter(visibility='visible')
    serializer_class = CompanyDetailSerializer
    permission_classes = (IsAuthenticated, )


# Create the company
class CompanyCreateAPIView(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyCreateSerializer
    permission_classes = (IsAuthenticated, )


# Retrieve, delete and update company
class CompanyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer
    # If user is able to manipulate the company
    permission_classes = [IsSuperUser | IsOwner | IsStaff ]
