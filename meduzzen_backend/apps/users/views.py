from companies import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import UsersRequests
from users.serializers import UsersRequestsSerializer


# Create your views here.
# All the user to company requests
class UsersRequestsModelViewSet(ModelViewSet):
    queryset = UsersRequests.objects.all()
    serializer_class = UsersRequestsSerializer
    permission_classes = (IsAuthenticated, )

    # If user is able to edit a request
    def get_permissions(self):
        if self.action in ['destroy', 'create']:
            self.permission_classes = (permissions.IsInvitedUser, )
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [permissions.IsInvitedUser | 
                                       permissions.IsUsersCompany ]
        return super().get_permissions()
    
    # Get current user list of requests to companies
    @action(detail=False, url_path='me', methods=['get'])
    def get_users_requests(self, request):
        queryset = UsersRequests.objects.filter(user=request.user)
        if not queryset:
            return Response({'detail': "No sent company requests"}, status.HTTP_404_NOT_FOUND)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Get all company join requests from users
    @action(detail=True, url_path='join_requests', 
            methods=['get'], permission_classes=(permissions.IsUsersCompany, ))
    def get_company_join_requests(self, request, pk=None):
        queryset = UsersRequests.objects.filter(company=pk)
        if not queryset:
            return Response({'detail': 
                             'There are no join requests to the company or the company does not exist'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
