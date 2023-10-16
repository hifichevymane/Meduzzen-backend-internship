# ruff: noqa: F401 F811 I001 F403
import pytest

from .fixtures.client import api_client, API_URL
from .fixtures.user_company_data import *

from companies.models import CompanyRequests, CompanyMembers

# Test user accept invite from company
@pytest.mark.django_db
def test_accept_invite(api_client, test_users, test_company):
    # Test user
    test_user = test_users[0]

    test_user_login_data = {
        'username': test_user.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_user_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    test_company_request_data = {
        'company': test_company,
        'user': test_user,
        'request_type': 'company to user'
    }

    # Create a company request
    company_request = CompanyRequests.objects.create(**test_company_request_data)

    test_accept_request_data = {
        'status': 'approved'
    }

    # Make the PATCH request to update status
    test_accept_request = api_client.patch(f'{API_URL}/company_requests/{company_request.id}/',
                                           **test_accept_request_data)
    assert test_accept_request.status_code == 200


# Test user decline invite from company
@pytest.mark.django_db
def test_decline_invite(api_client, test_users, test_company):
    # Test user
    test_user = test_users[0]

    test_user_login_data = {
        'username': test_user.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_user_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    test_company_request_data = {
        'company': test_company,
        'user': test_user,
        'request_type': 'company to user'
    }

    # Create a company request
    company_request = CompanyRequests.objects.create(**test_company_request_data)

    test_accept_request_data = {
        'status': 'rejected'
    }

    # Make the PATCH request to update status
    test_accept_request = api_client.patch(f'{API_URL}/company_requests/{company_request.id}/',
                                           **test_accept_request_data)
    assert test_accept_request.status_code == 200


# Test send request to company from user
@pytest.mark.django_db
def test_send_request_to_company(api_client, test_company, test_users):
    # Test user
    test_user = test_users[0]

    test_user_login_data = {
        'username': test_user.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_user_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    test_user_request_data = {
        'company': test_company.id,
        'user': test_user.id,
        'request_type': 'user to company'
    }
    # Send request from user to company and check if it is successful
    test_user_request = api_client.post(f'{API_URL}/users_requests/', test_user_request_data)
    assert test_user_request.status_code == 201


# Test send request to company from user
@pytest.mark.django_db
def test_decline_request_to_company(api_client, test_company, test_users):
    # Test user
    test_user = test_users[0]

    test_owner_login_data = {
        'username': test_user.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    test_user_request_data = {
        'company': test_company,
        'user': test_user,
        'request_type': 'user to company'
    }

    # Create a company request
    test_user_request = CompanyRequests.objects.create(**test_user_request_data)

    # Cancel the request to the company and check if it's successfull
    test_decline_request = api_client.delete(f'{API_URL}/users_requests/{test_user_request.id}/')
    print(test_decline_request)
    assert test_decline_request.status_code == 204


# Test user leave the company
@pytest.mark.django_db
def test_leave_company(api_client, test_company, test_users):
    # Test user
    test_user = test_users[0]

    test_owner_login_data = {
        'username': test_user.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    test_company_member_data = {
        'company': test_company,
        'user': test_user
    }

    # Create a new company member
    test_company_member = CompanyMembers.objects.create(**test_company_member_data)

    # DELETE request to leave the company and check if it was successful
    leave_company_request = api_client.delete(f'{API_URL}/company_members/{test_company_member.id}/')
    assert leave_company_request.status_code == 204
