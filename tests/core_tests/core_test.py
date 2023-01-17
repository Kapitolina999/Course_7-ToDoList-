import pytest
from django.urls import reverse

from core import serializers


@pytest.mark.django_db
def test_user_create(client):
    response = client.post(reverse('signup'),
                           data={'username': 'testname1',
                                 'email': 'test1@mail.ru',
                                 'password': '56po4gnkaW1',
                                 'password_repeat': '56po4gnkaW1'})

    # user = User.objects.get(pk=1)
    # expected_response = RegistrationSerializer(user).data
    expected_response = {
        'id': 1,
        'username': 'testname1',
        'first_name': '',
        'last_name': '',
        'email': 'test1@mail.ru',
        }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_login(client, new_user):
    response = client.post(reverse('login'),
                           data={"username": "testname1",
                                 "password": "56po4gnkaW1"}, content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_profile_retrieve(api_client, new_user):
    response = api_client.get(reverse('profile'))
    expected_response = serializers.ProfileSerializer(new_user).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_profile_delete(api_client):
    response = api_client.delete(reverse('profile'))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_password(api_client, new_user):
    response_change_password = api_client.put(reverse('update_password'),
                                              data={'new_password': 'cgd789poyt5!',
                                                    'old_password': '56po4gnkaW1'})

    assert response_change_password.status_code == 200
