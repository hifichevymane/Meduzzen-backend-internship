from companies.models import Company
from rest_framework.permissions import BasePermission

from users.models import UsersRequests


class HasUserNotSentRequestYet(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            company = request.data.get('company')
            user = request.user
            # Return true if user has not already sent request
            return not UsersRequests.objects.filter(company=company, user=user).exists()
        return False


class DoesUserSendRequestToHisCompany(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            user = request.user
            company = request.data.get('company')

            try:
                request_company = Company.objects.get(id=company)
                return request_company.owner != user
            except Company.DoesNotExist:
                return False
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.company.owner != user
