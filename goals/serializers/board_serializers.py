from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models.board import Board, BoardParticipant

User = get_user_model()


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.role_choices)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'board']


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ['id', 'created', 'updated']
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    participants = BoardParticipantSerializer(many=True)

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated']

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        participants = validated_data.pop('participants')
        participant_id = {participant['user'].id: participant for participant in participants}

        old_participants = instance.participants.exclude(user=owner)

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in participant_id:
                    old_participant.delete()
                else:
                    if old_participant.role != participant_id[old_participant.user_id]['role']:
                        old_participant.role = participant_id[old_participant.user_id]['role']
                        old_participant.save()
                    participant_id.pop(old_participant.user_id)
            for new_participant in participant_id.values():
                BoardParticipant.objects.create(board=instance, user=new_participant['user'],
                                                role=new_participant['role'])

            instance.title = validated_data['title']
            instance.save()

        return instance
