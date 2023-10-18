# ruff: noqa: F401 F811 I001 F403
import pytest
from django.contrib.auth import get_user_model

from companies.models import Company, CompanyInvitations, CompanyMembers
from users.models import UsersRequests

from model_bakery import baker

User = get_user_model()

# Create an owner
@pytest.fixture
def test_owner():
    # Owner data
    test_owner_user_data = {
        'username': 'test_owner',
        'email': 'test_owner@email.com',
        'first_name': 'test_owner',
        'last_name': 'test_owner',
        'password': 'DeathGrips228'
    }

    # Create the owner
    test_owner = User.objects.create_user(**test_owner_user_data)

    return test_owner


# Create a company
@pytest.fixture
def test_company(test_owner):
    # Create a company
    test_company_data = {
        "name": "Google",
        "description": "Google desc",
        "owner": test_owner
    }

    test_owner_company = Company.objects.create(**test_company_data)

    return test_owner_company


@pytest.fixture
def test_users():
    test_user_data1 = {
        'username': 'test_invited_user1',
        'email': 'test_invited_user1@email.com',
        'first_name': 'test_invited_user1',
        'last_name': 'test_invited_user1',
        'password': 'DeathGrips228'
    }

    test_user_data2 = {
        'username': 'test_invited_user2',
        'email': 'test_invited_user2@email.com',
        'first_name': 'test_invited_user2',
        'last_name': 'test_invited_user2',
        'password': 'DeathGrips228'
    }

    test_user_data3 = {
        'username': 'test_invited_user3',
        'email': 'test_invited_user3@email.com',
        'first_name': 'test_invited_user3',
        'last_name': 'test_invited_user3',
        'password': 'DeathGrips228'
    }

    # Create users
    test_user1 = User.objects.create_user(**test_user_data1)
    test_user2 = User.objects.create_user(**test_user_data2)
    test_user3 = User.objects.create_user(**test_user_data3)

    return test_user1, test_user2, test_user3


@pytest.fixture
def test_company_invite(test_users, test_company):
    test_user = test_users[0]

    test_company_request_data = {
        'company': test_company,
        'user': test_user,
    }

    # Create a company request
    company_request = CompanyInvitations.objects.create(**test_company_request_data)

    return company_request


@pytest.fixture
def test_user_request(test_users, test_company):
    test_user = test_users[0]

    # User request body
    test_user_request_data = {
        'company': test_company,
        'user': test_user,
    }

    # Create a user request
    test_user_request = UsersRequests.objects.create(**test_user_request_data)

    return test_user_request


@pytest.fixture
def test_company_member(test_users, test_company):
    test_user = test_users[0]

    test_company_member_data = {
        'company': test_company,
        'user': test_user
    }

    # Create a new company member
    test_company_member = CompanyMembers.objects.create(**test_company_member_data)

    return test_company_member


@pytest.fixture
def test_invites_payloads(test_users, test_company):
    test_invited_user1, test_invited_user2, test_invited_user3 = test_users

    # Invite the user to the company
    test_invite_user1_payload = {
        'user': test_invited_user1.id,
        'company': test_company.id,
    }

    test_invite_user2_payload = {
        'user': test_invited_user2.id,
        'company': test_company.id,
    }

    test_invite_user3_payload = {
        'user': test_invited_user3.id,
        'company': test_company.id,
    }

    payloads = (test_invite_user1_payload, 
                test_invite_user2_payload, 
                test_invite_user3_payload)

    return payloads
