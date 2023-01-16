import json

import pytest
from django.urls import reverse

from goals.serializers.board_serializers import BoardCreateSerializer


# @pytest.mark.django_db
# def test_bord_create(api_client, board):
#     data = {
#         "title": "board_1",
#     }
#     expected_response = BoardCreateSerializer(board).data
#     # response = api_client.post("/board/create/", data=data, content_type='application/json')
#     response = api_client.post(reverse("board_create"), data={"title": "board_1"})
#     response_data = response.data
#     assert response_data == expected_response
#     # assert response_data['is_deleted'] == expected_response['is_deleted']
#     # assert response_data['created'] == expected_response['created']
#     # assert response_data['updated'] == expected_response['updated']
#     assert response.status_code == 201