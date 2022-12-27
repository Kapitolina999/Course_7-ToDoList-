from django.contrib.auth import get_user_model
from django.db import models

from goals.models.category import GoalCategory

User = get_user_model()


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(verbose_name='Приоритет', choices=Priority.choices,
                                                default=Priority.medium)
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='goals', on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    title = models.CharField(verbose_name='Название', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True)
    due_date = models.DateField(verbose_name='Дата выполнения', null=True)
    category = models.ForeignKey(GoalCategory, verbose_name='Категория', related_name='goals', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
