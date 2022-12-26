from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models.goal import Goal


class Command(BaseCommand):
    help = 'Run telegrame bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TG_BOT_API_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            response = self.tg_client.get_updates(offset=offset)
            for item in response.result:
                offset = item.update_id + 1
                tg_user, created = TgUser.objects.get_or_create(tg_chat_id=item.message.chat.id,
                                                                tg_user_id=item.message.from_.id)

                if created:
                    tg_user.set_verification_code()
                    self.tg_client.send_message(tg_user.tg_chat_id,
                                                f'Привет. Подтвердите, пожалуйста, свой аккаунт. '
                                                f'Для подтверждения необходимо ввести код: '
                                                f'{tg_user.verification_code}')
                    continue

                elif not tg_user.user:
                    tg_user.set_verification_code()
                    self.tg_client.send_message(tg_user.tg_chat_id,
                                                f'Для дальнейшей работы подтвердите, пожалуйста, свой аккаунт. '
                                                f'Для подтверждения необходимо ввести код: '
                                                f'{tg_user.verification_code}')
                    continue

                if item.message.text == '/goals':
                    user = tg_user.user
                    goals = Goal.objects.filter(category__board__participants__user=user)

                    for goal in goals:
                        self.tg_client.send_message(tg_user.tg_chat_id,
                                                    f'Название {goal.title}, \n '
                                                    f'Категория {goal.category}, \n'
                                                    f'Статус {goal.get_status_display()}, \n'
                                                    f'Дедлайн {goal.due_date if goal.due_date else "Нет"} \n')

                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Неизвестная команда')


