from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Board(models.Model):
    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)


class BoardParticipant(models.Model):
    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='participants')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.PROTECT, related_name='participants')
    role = models.PositiveSmallIntegerField(verbose_name='Роль', choices=Role.choices, default=Role.owner)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    role_choices = Role.choices
    role_choices.pop(0)
