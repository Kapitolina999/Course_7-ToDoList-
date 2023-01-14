from django.contrib.auth.models import AbstractUser  # type: ignore


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
