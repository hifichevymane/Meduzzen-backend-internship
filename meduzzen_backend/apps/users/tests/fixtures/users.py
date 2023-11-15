# ruff: noqa: F401 F811 I001 F403
import pytest
from django.contrib.auth import get_user_model

from model_bakery import baker
from users.tests.schemas.users import UserModelSchema
from users.models import UsersRequests
from faker import Faker
from companies.tests.schemas.companies import CompanyInviteRequestBodySchema

User = get_user_model()
fake = Faker()

# Create an owner
@pytest.fixture
def test_owner():
    # Owner data
    test_owner_user_data = UserModelSchema(
        username='test_owner',
        email='test_owner@email.com',
        first_name='test_owner',
        last_name='test_owner',
        password='DeathGrips228'
    )

    # Create the owner
    test_owner = User.objects.create_user(**test_owner_user_data.model_dump())

    return test_owner


@pytest.fixture
def test_users():
    test_user_data_1 = UserModelSchema(
        username='test_invited_user1',
        email='test_invited_user1@email.com',
        first_name='test_invited_user1',
        last_name='test_invited_user1',
        password='DeathGrips228'
    )
    test_user_1 = User.objects.create_user(**test_user_data_1.model_dump())

    test_user_data_2 = UserModelSchema(
        username=fake.simple_profile()['username'],
        email=fake.simple_profile()['mail'],
        first_name=fake.simple_profile()['name'],
        last_name=fake.simple_profile()['name'],
        password='DeathGrips228'
    )
    test_user_2 = User.objects.create_user(**test_user_data_2.model_dump())
    
    test_user_3_data = UserModelSchema(
        username=fake.simple_profile()['username'],
        email=fake.simple_profile()['mail'],
        first_name=fake.simple_profile()['name'],
        last_name=fake.simple_profile()['name'],
        password='DeathGrips228'
    )
    test_user_3 = User.objects.create_user(**test_user_3_data.model_dump())

    return test_user_1, test_user_2, test_user_3


@pytest.fixture
def test_user_request(test_users, test_company):
    test_user = test_users[0]
    test_user_request : UsersRequests = baker.make(
        UsersRequests, user=test_user, 
        company=test_company
    )

    return test_user_request


@pytest.fixture
def test_invites_payloads(test_users, test_company):
    test_invited_user1, test_invited_user2, test_invited_user3 = test_users

    test_invite_user1_payload = CompanyInviteRequestBodySchema(
        user=test_invited_user1.id,
        company=test_company.id
    ).model_dump()

    test_invite_user2_payload = CompanyInviteRequestBodySchema(
        user=test_invited_user2.id,
        company=test_company.id
    ).model_dump()

    test_invite_user3_payload = CompanyInviteRequestBodySchema(
        user=test_invited_user3.id,
        company=test_company.id
    ).model_dump()

    payloads = (test_invite_user1_payload, 
                test_invite_user2_payload, 
                test_invite_user3_payload)

    return payloads
