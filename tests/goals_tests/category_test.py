import json

import pytest
from django.urls import reverse

from goals.serializers.category_serializers import GoalCategorySerializer
from tests.factories import ParticipantFactory, CategoryFactory


@pytest.mark.django_db
def test_category_create(api_client, new_user, board):
    ParticipantFactory(user=new_user, board=board)

    category = CategoryFactory.create(user=new_user)

    data = {
        'title': category.title,
        'board': board.pk
    }

    response = api_client.post(reverse('goal_category_create'), data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_category_list(api_client, new_user, board):
    ParticipantFactory(user=new_user, board=board)
    categories = CategoryFactory.create_batch(3, user=new_user, board=board)

    response = api_client.get(f'{reverse("goal_category_list")}?limit={len(categories)}')

    results = GoalCategorySerializer(categories, many=True).data

    expected_response = {
        'count': len(categories),
        'next': None,
        'previous': None,
        'results': list(map(lambda i: dict(i), results))
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_category_retrieve(api_client, new_user, board):
    ParticipantFactory(user=new_user, board=board)
    category = CategoryFactory(board=board, user=new_user)
    response = api_client.get(reverse('goal_category', args=[category.pk]))

    expected_response = GoalCategorySerializer(category).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_category_delete(api_client, new_user, board):
    ParticipantFactory(user=new_user, board=board)
    category = CategoryFactory(user=new_user, board=board)
    response = api_client.delete(reverse('goal_category', args=[category.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_category_update(api_client, new_user, board):
    ParticipantFactory(user=new_user, board=board)
    category = CategoryFactory(user=new_user, board=board)
    response = api_client.put(reverse('goal_category', args=[category.pk]), data={'title': 'new_category'})

    assert response.status_code == 200
    assert response.data['title'] == 'new_category'