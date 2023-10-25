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

from quizzes.tests.fixtures.quizzes import test_quiz_results, test_questions, test_quizzes, test_answer_options

from companies.models import CompanyMembers
from companies.enums import CompanyInvitationStatus, CompanyMemberRole
from users.models import UsersRequests
from users.enums import UsersRequestStatus

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


@pytest.mark.django_db
def test_cancel_request_to_company(user_api_client, test_user_request):
    test_cancel_request_data = {
        'status': UsersRequestStatus.CANCELED.value
    }

    request_id = test_user_request.id

    test_cancel_request = user_api_client.patch(f'{API_URL}/users_requests/{request_id}/',
                                                test_cancel_request_data)
    assert test_cancel_request.data['status'] == UsersRequestStatus.CANCELED.value
    assert test_cancel_request.status_code == 200


# Test user leave the company
@pytest.mark.django_db
def test_leave_company(user_api_client, test_company_member):
    leave_company_request = user_api_client.delete(f'{API_URL}/company_members/{test_company_member.id}/')
    
    assert leave_company_request.status_code == 204
    with pytest.raises(CompanyMembers.DoesNotExist):
        CompanyMembers.objects.get(pk=test_company_member.id)


# Test sending invites to company from not owner
@pytest.mark.django_db
def test_send_invite_from_not_owner(user_api_client, test_company, test_invites_payloads):
    test_invite_payload = test_invites_payloads[1]

    test_invite_request = user_api_client.post(f'{API_URL}/company_invites/', test_invite_payload)
    assert test_invite_request.status_code == 403


@pytest.mark.django_db
def test_send_request_from_company_member(user_api_client, test_company, test_company_member):
    user_request_payload = {
        'company': test_company.id
    }

    request = user_api_client.post(f'{API_URL}/users_requests/', user_request_payload)
    assert request.status_code == 403


@pytest.mark.django_db
def test_send_request_twice(user_api_client, test_user_request, test_company):
    request_payload = {
        'company': test_company.id
    }

    request = user_api_client.post(f'{API_URL}/users_requests/', request_payload)
    assert request.status_code == 403


@pytest.mark.django_db
def test_calculate_avarage_score_in_entire_system(user_api_client, test_quiz_results):
    request = user_api_client.get(f'{API_URL}/users/calculate_avarage_score/')

    assert request.status_code == 200
    # Check test_company_actions line 180 
    assert request.data['rating'] == 0.75
