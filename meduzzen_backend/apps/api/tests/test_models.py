import pytest
from django.contrib.auth import get_user_model

# # Get User model
User = get_user_model()

# Create your tests here.
@pytest.mark.django_db
def test_create_user():
    test_username = "sfdf"

    existing_user = User.objects.filter(username=test_username).first()
    assert existing_user is None # If user exists

    test_user = User.objects.create(username=test_username)

    test_users = User.objects.all()
    assert len(test_users) == 1
