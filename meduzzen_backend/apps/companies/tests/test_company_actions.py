# ruff: noqa: F401 F811 F403
import pytest
from api.tests.fixtures.client import API_URL, api_client
from quizzes.tests.fixtures.quizzes import test_answer_options, test_questions, test_quiz_results, test_quizzes
from users.enums import UsersRequestStatus
from users.tests.fixtures.user_client import user_api_client
from users.tests.fixtures.users import test_invites_payloads, test_owner, test_user_request, test_users
from users.tests.pydantic.users import UserRequestBody, UserRequestUpdateStatusBody

from companies.enums import CompanyInvitationStatus, CompanyMemberRole
from companies.models import CompanyInvitations, CompanyMembers
from companies.tests.fixtures.companies import test_company, test_company_invite, test_company_members
from companies.tests.pydantic.companies import (
    CompanyInviteUpdateStatusBody,
    CompanyMemberChangeRoleBody,
    CompanyMemberRatingBody,
)

from .fixtures.companies_client import owner_api_client


# Test send invite
@pytest.mark.django_db
def test_send_invitation_to_the_user(owner_api_client, test_invites_payloads):
    # Invite the user to the company
    test_invite_payload1, test_invite_payload2, test_invite_payload3 = test_invites_payloads

    response_test_invite1 = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        test_invite_payload1
    )
    
    assert response_test_invite1.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite1.data['id'])

    response_test_invite2 = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        test_invite_payload2
    )
    
    assert response_test_invite2.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite2.data['id'])
    
    response_test_invite3 = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        test_invite_payload3
    )
    
    assert response_test_invite3.status_code == 201
    assert CompanyInvitations.objects.get(pk=response_test_invite3.data['id'])


# Test invite revoke
@pytest.mark.django_db
def test_revoke_invite(owner_api_client, test_invites_payloads):
    # Invite the user
    test_invite_user_payload = test_invites_payloads[0]

    response_invite = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        test_invite_user_payload
    )
    assert response_invite.status_code == 201
    invite_id = response_invite.data['id']

    test_revoke_request_payload = CompanyInviteUpdateStatusBody(
        status= CompanyInvitationStatus.REVOKED.value
    )

    response_revoke = owner_api_client.patch(
        f'{API_URL}/company_invites/{invite_id}/',
        test_revoke_request_payload.model_dump()
    )
    
    assert response_revoke.status_code == 200
    assert response_revoke.data['status'] == CompanyInvitationStatus.REVOKED.value


# Test Owner approving request to the company
@pytest.mark.django_db
def test_approve_request(owner_api_client, test_user_request):
    # Test approve request
    test_approve_request_data = UserRequestUpdateStatusBody(
        status=UsersRequestStatus.ACCEPTED.value
    )

    test_approve_request = owner_api_client.patch(
        f'{API_URL}/users_requests/{test_user_request.id}/',
        test_approve_request_data.model_dump()
    )

    assert test_approve_request.status_code == 200
    assert test_approve_request.data['status'] == UsersRequestStatus.ACCEPTED.value


# Test Owner declining request to the company
@pytest.mark.django_db
def test_reject_request(owner_api_client, test_user_request):
    # Test reject request
    test_approve_request_data = UserRequestUpdateStatusBody(
        status=UsersRequestStatus.REJECTED.value
    )

    test_approve_request = owner_api_client.patch(
        f'{API_URL}/users_requests/{test_user_request.id}/',
        test_approve_request_data.model_dump()
    )

    assert test_approve_request.status_code == 200
    assert test_approve_request.data['status'] == UsersRequestStatus.REJECTED.value


# Test remove user from company
@pytest.mark.django_db
def test_remove_users_from_company(owner_api_client, test_company_members):
    test_company_member = test_company_members[0]

    # Remove user from company and check if request is successful
    remove_user_request = owner_api_client.delete(
        f'{API_URL}/company_members/{test_company_member.id}/'
    )
    
    assert remove_user_request.status_code == 204
    with pytest.raises(CompanyMembers.DoesNotExist): 
        CompanyMembers.objects.get(pk=test_company_member.id)


@pytest.mark.django_db
def test_send_invite_to_company_member(owner_api_client, test_company_members, test_invites_payloads):
    test_invite_payload = test_invites_payloads[0]
    test_invite_to_company_member = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        test_invite_payload
    )

    assert test_invite_to_company_member.status_code == 403


@pytest.mark.django_db
def test_send_invite_twice(owner_api_client, test_company_invite, test_invites_payloads):
    invite_payload = test_invites_payloads[0]

    request = owner_api_client.post(
        f'{API_URL}/company_invites/', 
        invite_payload
    )
    assert request.status_code == 403


@pytest.mark.django_db
def test_owner_send_request_to_his_company(owner_api_client, test_company):
    request_payload = UserRequestBody(company=test_company.id)

    request = owner_api_client.post(
        f'{API_URL}/users_requests/', 
        request_payload.model_dump()
    )
    assert request.status_code == 403

# Test apointing admin role and removing this role
@pytest.mark.parametrize("role", [CompanyMemberRole.ADMIN.value, CompanyMemberRole.MEMBER.value])
@pytest.mark.django_db
def test_appoint_remove_admin_role(role, owner_api_client, test_company_members):
    request_payload = CompanyMemberChangeRoleBody(role=role)

    test_company_member = test_company_members[0]

    request = owner_api_client.patch(
        f'{API_URL}/company_members/{test_company_member.id}/',
        request_payload.model_dump()
    )
    
    assert request.status_code == 200
    assert request.data['role'] == role


@pytest.mark.django_db
def test_calculate_avarage_score_in_company(user_api_client, test_quiz_results, 
                                            test_company, test_owner, test_users):
    test_user = test_users[0]

    test_company_user_rating_payload = CompanyMemberRatingBody(
        company=test_company.id,
        user=test_user.id
    )

    # Create company user rating
    test_company_user_rating_request = user_api_client.post(
        f'{API_URL}/company_user_ratings/',
        test_company_user_rating_payload.model_dump()
    )
    
    assert test_company_user_rating_request.status_code == 201
    assert test_company_user_rating_request.data['avarage_score'] == 0.0 # Default avarage score

    test_company_user_rating_id = test_company_user_rating_request.data['id']
    # PATCH request to calculate avarage score
    test_calculate_avarage_score_request = user_api_client.patch(
        f'{API_URL}/company_user_ratings/{test_company_user_rating_id}/')
    
    assert test_calculate_avarage_score_request.status_code == 200
    '''
    We have two quiz results, one quiz was completed with 2 correct answers out of 2
    Another quiz was completed with 1 correct answer out of 2
    
    To calculate avarage value:
    avarage_score = (2 + 1)/(2 + 2) = 3/4 = 0.75
    '''
    assert test_calculate_avarage_score_request.data['avarage_score'] == 0.75
