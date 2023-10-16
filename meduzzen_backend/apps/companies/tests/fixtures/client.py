# ruff: noqa: F401 F811 I001
import pytest
from rest_framework.test import APIClient

from .user_company_data import test_owner

API_URL = '/api/v1'

# API client
@pytest.fixture
def api_client(test_owner):
    return APIClient()
