# ruff: noqa: F401 F811 I001 F403
import pytest

from api.tests.fixtures.client import api_client, API_URL
from companies.tests.fixtures.companies import (
    test_company,
    test_company_member,
    test_company_invite)

from users.tests.fixtures.users import (
    test_users, 
    test_owner, 
    test_user_request, 
    test_invites_payloads)

from .fixtures.user_client import user_api_client

from companies.models import CompanyMembers
from companies.models import CompanyInvitationStatus
from users.models import UsersRequests, UsersRequestStatus

# Test user accept invite from company
@pytest.mark.django_db
def test_accept_invite(user_api_client, test_company_invite):
    test_accept_request_data = {
        'status': CompanyInvitationStatus.ACCEPTED.value
    }

    invite_id = test_company_invite.id

    test_accept_request = user_api_client.patch(f'{API_URL}/company_invites/{invite_id}/',
                                                test_accept_request_data)
    assert test_accept_request.data['status'] == CompanyInvitationStatus.ACCEPTED.value
    assert test_accept_request.status_code == 200


# Test user decline invite from company
@pytest.mark.django_db
def test_decline_invite(user_api_client, test_company_invite):
    test_accept_request_data = {
        'status': CompanyInvitationStatus.DECLINED.value
    }

    invite_id = test_company_invite.id

    test_accept_request = user_api_client.patch(f'{API_URL}/company_invites/{invite_id}/', 
                                                test_accept_request_data)
    assert test_accept_request.data['status'] == CompanyInvitationStatus.DECLINED.value
    assert test_accept_request.status_code == 200


# Test send request to company from user
@pytest.mark.django_db
def test_send_request_to_company(user_api_client, test_company):
    test_user_request_data = {
        'company': test_company.id,
    }

    test_user_request = user_api_client.post(f'{API_URL}/users_requests/', 
                                             test_user_request_data)
    
    assert test_user_request.status_code == 201
    assert UsersRequests.objects.get(pk=test_user_request.data['id'])


# Test revoke user request to the company
@pytest.mark.django_db
def test_revoke_request_to_company(user_api_client, test_user_request):
    test_revoke_request_data = {
        'status': UsersRequestStatus.REVOKED.value
    }

    request_id = test_user_request.id

    test_revoke_request = user_api_client.patch(f'{API_URL}/users_requests/{request_id}/',
                                                test_revoke_request_data)
    assert test_revoke_request.data['status'] == UsersRequestStatus.REVOKED.value
    assert test_revoke_request.status_code == 200


# Test user leave the company
@pytest.mark.django_db
def test_leave_company(user_api_client, test_company_member):
    leave_company_request = user_api_client.delete(f'{API_URL}/company_members/{test_company_member.id}/')
    
    assert leave_company_request.status_code == 204
    with pytest.raises(CompanyMembers.DoesNotExist):
        CompanyMembers.objects.get(pk=test_company_member.id)
