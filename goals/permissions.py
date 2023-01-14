from rest_framework import permissions

from goals.models.board import BoardParticipant, Board
from goals.models.category import GoalCategory
from goals.models.comment import Comment
from goals.models.goal import Goal


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Board) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj).exists()

        return BoardParticipant.objects.filter(user=request.user, board=obj, role=BoardParticipant.Role.owner).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: GoalCategory) -> bool:
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.board).exists()

        return BoardParticipant.objects.filter(user=request.user, board=obj.board,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                                               ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Goal) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=obj.category.board).exists()

        return BoardParticipant.objects.filter(user=request.user, board=obj.category.board,
                                               role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
                                               ).exists()


class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Comment) -> bool:

        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
