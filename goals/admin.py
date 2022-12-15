from django.contrib import admin

from goals.models.board import Board
from goals.models.comment import Comment
from goals.models.category import GoalCategory
from goals.models.goal import Goal


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'created', 'updated', 'category')
    search_fields = ('title', 'description', 'user')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'created', 'updated', 'goal')
    search_fields = ('text', 'user')


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated', 'is_deleted')
    search_fields = ('title',)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Board, BoardAdmin)
