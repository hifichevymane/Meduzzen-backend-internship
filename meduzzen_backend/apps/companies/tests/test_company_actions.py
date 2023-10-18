# ruff: noqa: F401 F811 I001 F403
import pytest

from api.tests.fixtures.client import api_client, API_URL
from companies.tests.fixtures.companies import (
    test_company,
    test_company_member)

from users.tests.fixtures.users import (
    test_users, 
    test_owner, 
    test_user_request, 
    test_invites_payloads)

from .fixtures.companies_client import owner_api_client

from companies.models import CompanyMembers, CompanyInvitationStatus, CompanyInvitations
from users.models import UsersRequestStatus

# Test send invite
@pytest.mark.django_db
def test_send_invitation_to_the_user(owner_api_client, test_invites_payloads):
    # Invite the user to the company
    test_invite_payload1, test_invite_payload2, test_invite_payload3 = test_invites_payloads

    response_test_invite1 = owner_api_client.post(f'{API_URL}/company_invites/', 
                                                  test_invite_payload1)
    
    assert response_test_invite1.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite1.data['id'])

    response_test_invite2 = owner_api_client.post(f'{API_URL}/company_invites/', 
                                                  test_invite_payload2)
    
    assert response_test_invite2.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite2.data['id'])
    
    response_test_invite3 = owner_api_client.post(f'{API_URL}/company_invites/', 
                                                  test_invite_payload3)
    
    assert response_test_invite3.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite3.data['id'])


# Test invite revoke
@pytest.mark.django_db
def test_revoke_invite(owner_api_client, test_invites_payloads):
    # Invite the user
    test_invite_user_payload = test_invites_payloads[0]

    response_invite = owner_api_client.post(f'{API_URL}/company_invites/', 
                                                test_invite_user_payload)
    assert response_invite.status_code == 201
    invite_id = response_invite.data['id']

    test_revoke_request_payload = {
        'status': CompanyInvitationStatus.REVOKED.value
    }

    response_revoke = owner_api_client.patch(f'{API_URL}/company_invites/{invite_id}/',
                                             test_revoke_request_payload)
    
    assert response_revoke.status_code == 200
    assert response_revoke.data['status'] == CompanyInvitationStatus.REVOKED.value


# Test Owner approving request to the company
@pytest.mark.django_db
def test_approve_request(owner_api_client, test_user_request):
    # Test approve request
    test_approve_request_data = {
        'status': UsersRequestStatus.ACCEPTED.value
    }

    test_approve_request = owner_api_client.patch(f'{API_URL}/users_requests/{test_user_request.id}/',
                                                  test_approve_request_data)

    assert test_approve_request.status_code == 200
    assert test_approve_request.data['status'] == UsersRequestStatus.ACCEPTED.value


# Test Owner declining request to the company
@pytest.mark.django_db
def test_reject_request(owner_api_client, test_user_request):
    # Test reject request
    test_approve_request_data = {
        'status': UsersRequestStatus.REJECTED.value
    }

    test_approve_request = owner_api_client.patch(f'{API_URL}/users_requests/{test_user_request.id}/',
                                                  test_approve_request_data)

    assert test_approve_request.status_code == 200
    assert test_approve_request.data['status'] == UsersRequestStatus.REJECTED.value


# Test remove user from company
@pytest.mark.django_db
def test_remove_users_from_company(owner_api_client, test_company_member):
    # Remove user from company and check if request is successful
    remove_user_request = owner_api_client.delete(f'{API_URL}/company_members/{test_company_member.id}/')
    
    assert remove_user_request.status_code == 204
    with pytest.raises(CompanyMembers.DoesNotExist): 
        CompanyMembers.objects.get(pk=test_company_member.id)
