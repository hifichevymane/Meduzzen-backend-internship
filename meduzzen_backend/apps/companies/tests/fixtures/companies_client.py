# ruff: noqa: F401 F811 I001 F403
import pytest

from api.tests.fixtures.client import api_client, API_URL
from companies.tests.fixtures.user_company_data import test_owner

@pytest.fixture
def owner_api_client(api_client, test_owner):
    test_owner_login_data = {
        'username': test_owner.username,
        'password': 'DeathGrips228',
    }

    # JWT auth
    auth_response = api_client.post(f'{API_URL}/auth/jwt/create/', test_owner_login_data)
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_response.data['access'])

    return api_client
