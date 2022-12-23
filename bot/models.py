from django.core.validators import MinLengthValidator
from django.db import models


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField()
    tg_user_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey('core.User', null=True, blank=True, default=None, verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    username = models.CharField(max_length=32, verbose_name='tg_username', blank=True,
                                validators=[MinLengthValidator(5)])

    class Meta:
        verbose_name = 'TG пользователь'
        verbose_name_plural = 'TG пользователи'

