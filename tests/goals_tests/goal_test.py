import json

import pytest
from django.urls import reverse

from goals.serializers.category_serializers import GoalCategorySerializer
from goals.serializers.goal_serializers import GoalSerializer
from tests.factories import ParticipantFactory, CategoryFactory, GoalFactory


@pytest.mark.django_db
def test_goal_create(api_client, new_user, board):
    category = CategoryFactory(board=board, user=new_user)
    goal = GoalFactory(user=new_user, category=category)
    ParticipantFactory(user=new_user, board=board)

    data = {
        'title': goal.title,
        'category': category.pk
    }

    response = api_client.post(reverse('goal_create'), data=json.dumps(data), content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_goal_delete(api_client, new_user, board):
    category = CategoryFactory(board=board, user=new_user)
    goal = GoalFactory(user=new_user, category=category)
    ParticipantFactory(user=new_user, board=board)

    response = api_client.delete(reverse('goal', args=[goal.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_goal_retrieve(api_client, new_user, board):
    category = CategoryFactory(board=board, user=new_user)
    goal = GoalFactory(user=new_user, category=category)
    ParticipantFactory(user=new_user, board=board)

    response = api_client.get(reverse('goal', args=[goal.pk]))
    expected_response = GoalSerializer(goal).data

    assert response.status_code == 200
    assert response.data == expected_response

