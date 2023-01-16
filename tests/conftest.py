import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from core.models import User
from tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def new_user(db):
    user = User.objects.create_user(
        username='testname1',
        email='test1@mail.ru',
        password='56po4gnkaW1'
    )
    return user


@pytest.fixture
def api_client(new_user):
    client = APIClient()
    client.login(username='testname1', password='56po4gnkaW1')
    return client



