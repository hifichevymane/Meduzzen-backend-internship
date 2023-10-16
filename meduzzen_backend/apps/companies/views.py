from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from companies import models, permissions, serializers


# Pagination class for CompanyModelViewSet
class CompanyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Create your views here.
# Company Model ViewSet
class CompanyModelViewSet(ModelViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanyModelSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CompanyPagination

    # Assign custom permission classes for PUT PATCH DELETE requests
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsSuperUser | 
                                       permissions.IsOwner | 
                                       permissions.IsStaff ]
        return super().get_permissions()

    # Override list method to list only visible companies
    def list(self, request, *args, **kwargs):
        queryset = models.Company.objects.filter(visibility='visible')
        page = self.paginate_queryset(queryset) # Paginate queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanyRequestsModelViewSet(ModelViewSet):
    queryset = models.CompanyRequests.objects.filter(request_type='company to user')
    serializer_class = serializers.CompanyRequestsModelSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit a request
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            self.permission_classes = (permissions.IsUsersCompany, )
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsUsersCompany | 
                                       permissions.IsInvitedUser]
        return super().get_permissions()
    
    # Get current user's list of invitations to companies
    @action(detail=False, url_path='me', methods=['get'])
    def get_companies_invitations(self, request):
        queryset = models.CompanyRequests.objects.filter(user=request.user,
                                                         request_type='company to user')
        
        if not queryset:
            return Response({'detail': "You have no invitations to companies"}, 
                            status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get company list of invited users by id
    @action(detail=True, url_path='invited_users', methods=['get'],
            permission_classes=(permissions.IsUsersCompany, ))
    def get_my_invited_users(self, request, pk=None):
        queryset = models.CompanyRequests.objects.filter(company=pk, 
                                                         request_type='company to user')
        if not queryset:
            return Response({'detail': 'There are no invited users or the company does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# All the user to company requests
class UsersRequestsModelViewSet(ModelViewSet):
    queryset = models.CompanyRequests.objects.filter(request_type='user to company')
    serializer_class = serializers.CompanyRequestsModelSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit a request
    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = (permissions.IsInvitedUser, )
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = (permissions.IsUsersCompany, )
        return super().get_permissions()
    
    # Get current user list of requests to companies
    @action(detail=False, url_path='me', methods=['get'])
    def get_users_requests(self, request):
        queryset = models.CompanyRequests.objects.filter(user=request.user, 
                                                         request_type='user to company')
        if not queryset:
            return Response({'detail': "No sent company requests"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get all company join requests from users
    @action(detail=True, url_path='join_requests', 
            methods=['get'], permission_classes=(permissions.IsUsersCompany, ))
    def get_company_join_requests(self, request, pk=None):
        queryset = models.CompanyRequests.objects.filter(company=pk, 
                                                         request_type='user to company')
        if not queryset:
            return Response({'detail': 
                             'There are no join requests to the company or the company does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# All members of Company
class CompanyMembersModelViewSet(ModelViewSet):
    queryset = models.CompanyMembers.objects.all()
    serializer_class = serializers.CompanyMembersModelSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit company members list
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = (permissions.IsUsersCompany, )
        elif self.action == 'destroy':
            self.permission_classes = [permissions.IsUsersCompany | 
                                       permissions.IsInvitedUser]
        return super().get_permissions()

    # Get all companies members list by company_id /company_members/id/members_list/
    @action(detail=True, url_path='members_list', methods=['get'])
    def company(self, request, pk=None):
        queryset = models.CompanyMembers.objects.filter(company=pk)

        if not queryset:
            return Response({'detail': "Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
