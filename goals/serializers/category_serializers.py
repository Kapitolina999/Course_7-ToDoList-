from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models.board import BoardParticipant
from goals.models.category import GoalCategory

User = get_user_model()


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # скрытое поле

    class Meta:
        model = GoalCategory
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_board(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted board')

        participant = BoardParticipant.objects.filter(board=value,
                                                      role__in=[BoardParticipant.Role.owner,
                                                                BoardParticipant.Role.writer],
                                                      user=self.context['request'].user).exists()

        if not participant:
            raise serializers.ValidationError('not owner or writer of board')

        return value


class GoalCategorySerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated', 'user', 'board']

