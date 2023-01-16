import factory

from core.models import User
from goals.models.board import Board, BoardParticipant
from goals.models.category import GoalCategory
from goals.models.comment import Comment
from goals.models.goal import Goal


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'testname%s' % n)
    email = factory.Sequence(lambda n: 'test%s@mail.ru' % n)
    password = '56po4gnkaW1'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Sequence(lambda n: 'board_%s' % n)


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Sequence(lambda n: 'category_%s' % n)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Sequence(lambda n: 'goal_%s' % n)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = 'test_comment_text'
