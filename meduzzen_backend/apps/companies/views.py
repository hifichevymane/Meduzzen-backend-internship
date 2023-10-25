from api.pagination import CommonPagination
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from companies.enums import CompanyMemberRole, Visibility
from companies.models import Company, CompanyInvitations, CompanyMembers, CompanyUserRating
from companies.permissions import (
    DoesOwnerSendInviteToItself,
    HasOwnerNotSentInviteYet,
    IsAbleToDeleteCompanyUserRating,
    IsInvitedUser,
    IsOwner,
    IsStaff,
    IsSuperUser,
    IsUserNotCompanyMember,
    IsUsersCompany,
)
from companies.serializers import (
    CompanyInvitationsModelSerializer,
    CompanyMembersModelSerializer,
    CompanyModelSerializer,
    CompanyUserRatingModelSerializer,
)


# Create your views here.
# Company Model ViewSet
class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CommonPagination

    # Assign custom permission classes for PUT PATCH DELETE requests
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSuperUser | 
                                       IsOwner | 
                                       IsStaff ]
        return super().get_permissions()

    # Override list method to list only visible companies
    def list(self, request, *args, **kwargs):
        queryset = Company.objects.filter(visibility=Visibility.VISIBLE.value)
        page = self.paginate_queryset(queryset) # Paginate queryset
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CompanyInvitationsModelViewSet(ModelViewSet):
    queryset = CompanyInvitations.objects.all()
    serializer_class = CompanyInvitationsModelSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit a request
    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = (IsUsersCompany, )
        elif self.action == 'create':
            self.permission_classes = (IsUsersCompany, 
                                       IsUserNotCompanyMember,
                                       HasOwnerNotSentInviteYet,
                                       DoesOwnerSendInviteToItself )
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsUsersCompany | 
                                       IsInvitedUser]
        return super().get_permissions()
    
    # Get current user's list of invitations to companies
    @action(detail=False, url_path='me', methods=['get'])
    def get_companies_invitations(self, request):
        queryset = CompanyInvitations.objects.filter(user=request.user)
        
        if not queryset:
            return Response({'detail': "You have no invitations to companies"}, 
                            status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get company list of invited users by id
    @action(detail=True, url_path='invited_users', methods=['get'],
            permission_classes=(IsUsersCompany, ))
    def get_my_invited_users(self, request, pk=None):
        queryset = CompanyInvitations.objects.filter(company=pk)
        if not queryset:
            return Response({'detail': 'There are no invited users or the company does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# All members of Company
class CompanyMembersModelViewSet(ModelViewSet):
    queryset = CompanyMembers.objects.all()
    serializer_class = CompanyMembersModelSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit company members list
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = (IsUsersCompany, )
        elif self.action == 'destroy':
            self.permission_classes = [IsUsersCompany | 
                                       IsInvitedUser]
        return super().get_permissions()

    # Get all companies members list by company_id /company_members/id/members_list/
    @action(detail=True, url_path='members_list', methods=['get'])
    def company_members_list(self, request, pk=None):
        queryset = CompanyMembers.objects.filter(company=pk)

        if not queryset:
            return Response({'detail': "Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get all company admin list by company_id
    @action(detail=True, url_path='admin_list', methods=['get'])
    def company_admin_list(self, request, pk=None):
        queryset = CompanyMembers.objects.filter(company=pk, 
                                                 role=CompanyMemberRole.ADMIN.value)
        
        if not queryset:
            return Response({'detail': "Not found"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyUserRatingModelViewSet(ModelViewSet):
    queryset = CompanyUserRating.objects.all()
    serializer_class = CompanyUserRatingModelSerializer
    permission_classes = (IsAuthenticated, )

    def get_permissions(self):
        if self.action == 'destroy':
            self.permission_classes = (IsAbleToDeleteCompanyUserRating, )
        return super().get_permissions()
