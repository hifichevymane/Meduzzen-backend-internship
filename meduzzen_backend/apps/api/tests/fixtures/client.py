# ruff: noqa: F401 F811 I001
import pytest
from rest_framework.test import APIClient

API_URL = '/api/v1'

# API client
@pytest.fixture
def api_client():
    return APIClient()
