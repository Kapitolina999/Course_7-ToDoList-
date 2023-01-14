from django.db import models

import string
import random


class TgUser(models.Model):
    tg_chat_id = models.BigIntegerField()
    tg_user_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey('core.User', null=True, blank=True, verbose_name='Пользователь', on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True, null=True, blank=True)

    def set_verification_code(self) -> None:
        code = string.digits + string.ascii_letters
        verification_code = ''

        for _ in range(6):
            verification_code += code[random.randrange(0, len(code))]

        self.verification_code = verification_code
        self.save()

    class Meta:
        verbose_name = 'TG пользователь'
        verbose_name_plural = 'TG пользователи'

