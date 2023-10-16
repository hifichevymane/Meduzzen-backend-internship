# ruff: noqa: F401 F811 I001 F403
import pytest
from django.contrib.auth import get_user_model

from .fixtures.client import api_client, API_URL
from .fixtures.user_company_data import *

from companies.models import CompanyRequests, CompanyMembers

User = get_user_model()

# Test send invite
@pytest.mark.django_db
def test_send_invitation_to_the_user(api_client, test_company, test_owner, test_users):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    # Several users to invite
    test_invited_user1, test_invited_user2, test_invited_user3 = test_users

    # Invite the user to the company
    test_invite_user1_payload = {
        'user': test_invited_user1.id,
        'company': test_company.id,
        'request_type': 'company to user'
    }

    test_invite_user2_payload = {
        'user': test_invited_user2.id,
        'company': test_company.id,
        'request_type': 'company to user'
    }

    test_invite_user3_payload = {
        'user': test_invited_user3.id,
        'company': test_company.id,
        'request_type': 'company to user'
    }

    response_test_invite1 = api_client.post(f'{API_URL}/company_requests/', 
                                            test_invite_user1_payload)
    assert response_test_invite1.status_code == 201

    response_test_invite2 = api_client.post(f'{API_URL}/company_requests/', 
                                            test_invite_user2_payload)
    assert response_test_invite2.status_code == 201
    
    response_test_invite3 = api_client.post(f'{API_URL}/company_requests/', 
                                            test_invite_user3_payload)
    assert response_test_invite3.status_code == 201


# Test invite revoke
@pytest.mark.django_db
def test_revoke_invite(api_client, test_company, test_owner, test_users):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    # Test user
    test_invited_user = test_users[0]

    # Invite the user
    test_invite_user_payload = {
        'user': test_invited_user.id,
        'company': test_company.id,
        'request_type': 'company to user'
    }

    response_invite = api_client.post(f'{API_URL}/company_requests/', test_invite_user_payload)
    assert response_invite.status_code == 201
    invite_id = response_invite.data['id']

    # Revoke the invite
    response_revoke = api_client.delete(f'{API_URL}/company_requests/{invite_id}/')
    assert response_revoke.status_code == 204


# Test Owner approving request to the company
@pytest.mark.django_db
def test_approve_request(api_client, test_company, test_owner, test_users):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    # Test user
    test_user = test_users[0]

    # User request body
    test_user_request_data = {
        'company': test_company,
        'user': test_user,
        'request_type': 'user to company',
    }

    # Create a user request
    test_user_request = CompanyRequests.objects.create(**test_user_request_data)
    assert test_user_request

    # Test approve request
    test_approve_request_data = {
        'status': 'approved'
    }

    test_approve_request = api_client.patch(f'{API_URL}/users_requests/{test_user_request.id}/',
                                            **test_approve_request_data)
    # Check if the request is successful
    assert test_approve_request.status_code == 200


# Test Owner approving request to the company
@pytest.mark.django_db
def test_reject_request(api_client, test_company, test_owner, test_users):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    # Test user
    test_user = test_users[0]

    # User request body
    test_user_request_data = {
        'company': test_company,
        'user': test_user,
        'request_type': 'user to company',
    }

    # Create a user request
    test_user_request = CompanyRequests.objects.create(**test_user_request_data)
    assert test_user_request

    # Test reject request
    test_approve_request_data = {
        'status': 'rejected'
    }

    test_approve_request = api_client.patch(f'{API_URL}/users_requests/{test_user_request.id}/',
                                            **test_approve_request_data)
    # Check if the request is successful
    assert test_approve_request.status_code == 200


# Test remove user from company
@pytest.mark.django_db
def test_remove_users_from_company(api_client, test_owner, test_company, test_users):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    # Test company member
    test_user = test_users[0]

    test_company_member_data = {
        'company': test_company,
        'user': test_user
    }

    # Create new member
    test_company_member = CompanyMembers.objects.create(**test_company_member_data)

    # Remove user from company and check if request is successful
    remove_user_request = api_client.delete(f'{API_URL}/company_members/{test_company_member.id}/')
    assert remove_user_request.status_code == 204
