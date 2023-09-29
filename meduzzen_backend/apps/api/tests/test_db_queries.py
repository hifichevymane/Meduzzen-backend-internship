import pytest
from api.models import User

# Create your tests here.
@pytest.mark.django_db
def test_queries_to_db():
    User.objects.create(username="sfdf")

    users = User.objects.all()
    assert len(users) == 1
