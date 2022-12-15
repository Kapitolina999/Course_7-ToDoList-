from django.urls import path

from goals.views.board_views import BoardCreateView, BoardListView, BoardView
from goals.views.category_views import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.comment_views import CommentCreateView, CommentListView, CommentView
from goals.views.goal_views import GoalCreateView, GoalListView, GoalView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='goal_category_create'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='goal_category_list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='goal_category'),
    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal'),
    path('goal_comment/create', CommentCreateView.as_view(), name='comment_create'),
    path('goal_comment/list', CommentListView.as_view(), name='comment_list'),
    path('goal_comment/<pk>', CommentView.as_view(), name='comment'),
    path('board/create', BoardCreateView.as_view(), name='board_create'),
    path('board/list', BoardListView.as_view(), name='board_list'),
    path('board/<pk>', BoardView.as_view(), name='board'),

]