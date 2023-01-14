from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models.board import BoardParticipant
from goals.models.comment import Comment
from goals.models.goal import Goal

User = get_user_model()


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user']

    def validate_goal(self, value: Goal) -> Goal:
        if not BoardParticipant.objects.filter(board_id=value.category.board_id, 
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                                               user=self.context['request'].user).exists():
            raise serializers.ValidationError('must be owner or writer')
        return value


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        read_only_fields = ['id', 'created', 'updated', 'user', 'goal']
        fields = '__all__'
