from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.models import User
from api.serializers import UserSerializer
import logging

# Create a logger
test_logger = logging.getLogger('main')

# Create your views here.
# health_check endpoint
@api_view(['GET'])
def health_check(request):
    response = {'status_code': 200, 'detail': 'ok', 'result': 'working'}
    # Execute logger message
    test_logger.info('Test logging')
    return Response(response)


# User ModelViewSet to make CRUD operations
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
