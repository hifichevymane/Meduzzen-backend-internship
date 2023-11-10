# ruff: noqa: F401 F811 I001 F403
import pytest

from model_bakery import baker

from users.tests.fixtures.users import test_owner, test_users
from companies.models import CompanyMembers, Company, CompanyInvitations


# Create a company
@pytest.fixture
def test_company(test_owner):
    # Create a company
    test_owner_company: Company = baker.make(Company, owner=test_owner)

    return test_owner_company


@pytest.fixture
def test_company_invite(test_users, test_company):
    test_user = test_users[0]
    company_request: CompanyInvitations = baker.make(CompanyInvitations, user=test_user, 
                                 company=test_company)

    return company_request


@pytest.fixture
def test_company_members(test_users, test_company):
    test_user_1, test_user_2, = test_users[0], test_users[1]

    test_company_member_1: CompanyMembers = baker.make(
        CompanyMembers, 
        user=test_user_1, 
        company=test_company
    )
    test_company_member_2: CompanyMembers = baker.make(
        CompanyMembers, 
        user=test_user_2, 
        company=test_company
    )

    return test_company_member_1, test_company_member_2
