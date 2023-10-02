import pytest
from django.contrib.auth import get_user_model

# Get User model
User = get_user_model()

# Create your tests here.
@pytest.mark.django_db
def test_create_user():
    username = "sfdf"

    existing_user = User.objects.filter(username=username).first()
    assert existing_user is None # If user exists

    user = User.objects.create(username=username)

    users = User.objects.all()
    assert len(users) == 1
