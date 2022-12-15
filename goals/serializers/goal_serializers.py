from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.serializers import ProfileSerializer
from goals.models.board import BoardParticipant
from goals.models.category import GoalCategory
from goals.models.goal import Goal

User = get_user_model()


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    category = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())

    class Meta:
        model = Goal
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if not BoardParticipant.objects.filter(board_id=value.board_id,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                                               user=self.context['request'].user).exists():
            raise serializers.ValidationError('not owner or writer of category')

        return value


class GoalSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = '__all__'

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if self.instance.category.board_id != value.board_id:
            raise serializers.ValidationError('сan not move between boards')
        return value

