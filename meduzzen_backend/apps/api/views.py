from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
# health_check endpoint
@api_view(['GET'])
def health_check(request):
    response = {'status_code': 200, 'detail': 'ok', 'result': 'working'}
    return Response(response)
