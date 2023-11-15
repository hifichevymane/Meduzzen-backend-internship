from companies.permissions import IsInvitedUser, IsUserNotCompanyMember, IsUsersCompany
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import UsersRequests
from users.permissions import DoesUserSendRequestToHisCompany, HasUserNotSentRequestYet
from users.serializers import UsersRequestsReadSerializer, UsersRequestsWriteSerializer


# Create your views here.
# All the user to company requests
class UsersRequestsModelViewSet(ModelViewSet):
    queryset = UsersRequests.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = UsersRequestsReadSerializer

    # Use different serializers to write/retrieve data
    def get_serializer_class(self):
        if self.action in ['create']:
            return UsersRequestsWriteSerializer
        return UsersRequestsReadSerializer

    # If user is able to edit a request
    def get_permissions(self):
        if self.action in ['destroy']:
            self.permission_classes = (IsInvitedUser, )
        elif self.action == 'create':
            self.permission_classes = (IsInvitedUser,
                                       IsUserNotCompanyMember,
                                       HasUserNotSentRequestYet,
                                       DoesUserSendRequestToHisCompany)
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsInvitedUser | 
                                       IsUsersCompany ]
        return super().get_permissions()
    
    # Get current user list of requests to companies
    @action(detail=False, url_path='me', methods=['get'])
    def get_users_requests(self, request):
        queryset = UsersRequests.objects.filter(user=request.user)
        if not queryset:
            return Response({'detail': "No sent company requests"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get all company join requests from users
    @action(detail=True, url_path='join_requests', 
            methods=['get'], permission_classes=(IsUsersCompany, ))
    def get_company_join_requests(self, request, pk=None):
        queryset = UsersRequests.objects.filter(company=pk)
        if not queryset:
            return Response(
                {'detail': 'There are no join requests to the company or the company does not exist'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
