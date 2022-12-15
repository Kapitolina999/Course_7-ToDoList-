from django.contrib.auth import get_user_model
from django.db import models

from goals.models.goal import Goal

User = get_user_model()


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата последнего обновления', auto_now=True)
    text = models.TextField(verbose_name='Текст')
    goal = models.ForeignKey(Goal, verbose_name='Цель', on_delete=models.PROTECT)


# class Question(models.Model):
#     text = models.TextField()
#     # ...
#
# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     # ...
#
#     class Meta:
#         order_with_respect_to = 'question'