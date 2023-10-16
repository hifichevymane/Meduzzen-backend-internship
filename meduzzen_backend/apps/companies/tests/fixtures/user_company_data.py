import pytest
from django.contrib.auth import get_user_model

from companies.models import Company

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
