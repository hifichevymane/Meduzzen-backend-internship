# ruff: noqa: F401 F811 I001 F403
import pytest

from model_bakery import baker

from users.tests.fixtures.users import test_owner, test_users


# Create a company
@pytest.fixture
def test_company(test_owner):
    # Create a company
    test_owner_company = baker.make('companies.Company', owner=test_owner)

    return test_owner_company


@pytest.fixture
def test_company_invite(test_users, test_company):
    test_user = test_users[0]
    company_request = baker.make('companies.CompanyInvitations', user=test_user, 
                                 company=test_company)

    return company_request


@pytest.fixture
def test_company_member(test_users, test_company):
    test_user = test_users[0]
    test_company_member = baker.make('companies.CompanyMembers', user=test_user, 
                                     company=test_company)

    return test_company_member
