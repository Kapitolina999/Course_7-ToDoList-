from django.contrib.auth import get_user_model
from django.db import models

from goals.models.board import Board

User = get_user_model()


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    board = models.ForeignKey(Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories')

    def __str__(self):
        return self.title
