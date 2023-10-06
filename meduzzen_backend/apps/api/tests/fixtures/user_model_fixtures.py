import pytest


# Init test user data fixture
@pytest.fixture
def test_user_data():
    test_data = {
        'username': "babka_v_kedah",
        'first_name': "Antonina",
        'last_name': "Zelenskiy",
        'email': "babka@gmail.com",
        'password': "Dhfdsdsdvb123435"
    }

    return test_data
