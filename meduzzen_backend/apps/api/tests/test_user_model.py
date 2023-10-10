import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from .fixtures.user_model_fixtures import test_user_data  #noqa: F401

# # Get User model
User = get_user_model()

# Create your tests here.
# Test user creation with not all required fields
@pytest.mark.django_db
def test_create_user_fail():
    test_username = "babka_v_kedah"

    # If raises error - test succeeded
    with pytest.raises(TypeError):
        User.objects.create_user(username=test_username)


# Test user creation with all required fields
@pytest.mark.django_db
def test_create_user_success(test_user_data): #noqa: F811
    assert User.objects.create_user(**test_user_data)


# Test user creation if username and email already exist
@pytest.mark.django_db
def test_create_existing_user():
    test_user_data1 = {
        'username': "babka_v_kedah",
        'first_name': "Maks",
        'last_name': "Kornishon",
        'email': "borov@gmail.com",
        'password': "Dhfdsdsdvb123435"
    }

    User.objects.create_user(**test_user_data1)

    # Create user with the same username and email
    test_user_data2 = {
        'username': "babka_v_kedah",
        'first_name': "Ivan",
        'last_name': "Vanya",
        'email': "borov@gmail.com",
        'password': "Dhfdsdsdvb123435"
    }

    # If raises error - test succeeded
    with pytest.raises(IntegrityError):
        User.objects.create_user(**test_user_data2)
