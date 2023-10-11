import pytest
from django.contrib.auth import get_user_model

from companies.models import Company

User = get_user_model()

@pytest.mark.django_db
def test_company_creation():
    test_name = "Test company"
    test_description = "Test description"

    test_user_data = {
        'username': "babka_v_kedah",
        'first_name': "Maks",
        'last_name': "Kornishon",
        'email': "borov@gmail.com",
        'password': "Dhfdsdsdvb123435"
    }

    test_user_instance = User.objects.create_user(**test_user_data)

    assert Company.objects.create(owner=test_user_instance,
                                  name=test_name, 
                                  description=test_description)
