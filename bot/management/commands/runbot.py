from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message


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
                offset += item.update_id
                self.handle_message(item.message)

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(tg_id=message.from_.id,
                                                        defaults={'tg_chat_id': message.chat.id,
                                                                  'username': message.from_.username})
        if created:
            self.tg_client.send_message(message.chat.id, '[greeting]')

        if tg_user.user:
            self.handle_verified_user(message, tg_user)
        else:
            self.handle_user_without_verification(message, tg_user)

    def handle_user_without_verification(self, message: Message, tg_user: TgUser):
        tg_user.set_verification_code()
        tg_user.save(update_fields=['verification_code'])
        self.tg_client.send_message(
            message.chat.id, f'[verification code] {tg_user.verification_code}'
        )

    def fetch_tasks(self, message: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_message = [f'#{item.id} {item.title}' for item in gls]
            self.tg_client.send_message(message.chat.id, '\n'.join(resp_message))
        else:
            self.tg_client.send_message(message.chat.id, '[goals list is empty]')

    def handle_verified_user(self, message: Message, tg_user: TgUser):
        if not message.text:
            return
        if '/goals' in message.text:
            self.fetch_tasks(message, tg_user)
        else:
            self.tg_client.send_message(message.chat.id, '[unknown command]')



