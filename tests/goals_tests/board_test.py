import json

import pytest
from django.urls import reverse

from goals.serializers.board_serializers import BoardListSerializer, BoardSerializer
from tests.factories import BoardFactory, ParticipantFactory


@pytest.mark.django_db
def test_board_create(api_client, new_user, board):
    ParticipantFactory.create(board=board, user=new_user)

    data = {'title': board.title}
    response = api_client.post(reverse('board_create'), data=json.dumps(data), content_type='application/json')

    expected_response = {
        'id': 2,
        'title': 'board_1',
        'is_deleted': False
    }

    assert response.status_code == 201
    assert response.data['id'] == expected_response['id']
    assert response.data['title'] == expected_response['title']
    assert response.data['is_deleted'] == expected_response['is_deleted']


@pytest.mark.django_db
def test_board_list(api_client, new_user):
    boards = BoardFactory.create_batch(3)

    for board in boards:
        ParticipantFactory.create(board=board, user=new_user)

    results = BoardListSerializer(boards, many=True).data
    response = api_client.get(f'{reverse("board_list")}?limit={len(boards)}')

    expected_response = {
        'count': len(boards),
        'next': None,
        'previous': None,
        'results': list(map(lambda i: dict(i), results))
    }

    assert response.status_code == 200
    assert response.json() == expected_response


@pytest.mark.django_db
def test_board_retrieve(api_client, new_user, board):
    participant = ParticipantFactory(user=new_user, board=board)
    response = api_client.get(reverse('board', args=[board.pk]))

    expected_response = BoardSerializer(board).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_board_update(api_client, new_user, board):
    participant = ParticipantFactory(user=new_user, board=board)
    response = api_client.put(reverse('board', args=[board.pk]),
                              data=json.dumps({'title': 'new_board', 'participants': []}),
                              content_type='application/json')

    assert response.status_code == 200
    assert response.data['title'] == 'new_board'


@pytest.mark.django_db
def test_board_delete(api_client, new_user, board):
    participant = ParticipantFactory(user=new_user, board=board)
    response = api_client.delete(reverse('board', args=[board.pk]))

    assert response.status_code == 204