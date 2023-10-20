# ruff: noqa: F401 F811 I001 F403
import pytest
from django.contrib.auth import get_user_model

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


@pytest.fixture
def test_users():
    test_user_data1 = {
        'username': 'test_invited_user1',
        'email': 'test_invited_user1@email.com',
        'first_name': 'test_invited_user1',
        'last_name': 'test_invited_user1',
        'password': 'DeathGrips228'
    }

    test_user1 = User.objects.create_user(**test_user_data1)
    test_user2 = baker.make('api.User')
    test_user3 = baker.make('api.User')

    return test_user1, test_user2, test_user3


@pytest.fixture
def test_user_request(test_users, test_company):
    test_user = test_users[0]
    test_user_request = baker.make('users.UsersRequests', user=test_user, 
                                   company=test_company)

    return test_user_request


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
