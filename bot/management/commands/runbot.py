from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError

from bot.models import TgUser
from bot.tg.client import TgClient
from goals.models.category import GoalCategory
from goals.models.goal import Goal


class Command(BaseCommand):
    help = 'Run telegrame bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.TG_BOT_API_TOKEN)
        self.offset = 0

    def handle(self, *args, **kwargs):

        while True:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1
                tg_user: TgUser | False = self.check_user(item.message)

                if not tg_user:
                    continue

                if item.message.text == '/goals':
                    self.get_goals(tg_user)
                elif item.message.text == '/create':
                    self.choice_category(tg_user)
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Для просмотра списка задач введи /goals.\n'
                                                                    'Для создания задачи введи /create.')

    def check_user(self, message):
        tg_user, created = TgUser.objects.get_or_create(tg_chat_id=message.chat.id, tg_user_id=message.from_.id)

        if created or not tg_user.user:

            try:
                tg_user.set_verification_code()
            except IntegrityError as e:
                tg_user.set_verification_code()

            self.tg_client.send_message(tg_user.tg_chat_id,
                                        f'Привет. Подтверди, пожалуйста, свой аккаунт. '
                                        f'Для подтверждения необходимо ввести код в приложении: '
                                        f'{tg_user.verification_code}')
            return False
        return tg_user

    def get_goals(self, tg_user):
        goals = Goal.objects.filter(user=tg_user.user, status__in=[1, 2, 3])

        if goals.count() > 0:
            [self.tg_client.send_message(tg_user.tg_chat_id,
                                         f'Название {goal.title},\n'
                                         f'Категория {goal.category},\n'
                                         f'Статус {goal.get_status_display()},\n'
                                         f'Дедлайн {goal.due_date if goal.due_date else "Нет"} \n') for goal in goals]
        else:
            self.tg_client.send_message(tg_user.tg_chat_id, 'Нет задач')

    def choice_category(self, tg_user):
        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user, is_deleted=False)
        self.tg_client.send_message(tg_user.tg_chat_id, 'Выбери категорию:')
        [self.tg_client.send_message(tg_user.tg_chat_id, category.title) for category in categories]
        self.tg_client.send_message(tg_user.tg_chat_id, 'Для отмены введи /cancle')
        dict_categories = {item.title: item for item in categories}

        flag = True
        while flag:
            response = self.tg_client.get_updates(offset=self.offset)
            for item in response.result:
                self.offset = item.update_id + 1

                if item.message.text in dict_categories:
                    category = dict_categories.get(item.message.text)
                    self.create_goal(tg_user, category)
                    flag = False
                elif item.message.text == '/cancle':
                    flag = False
                else:
                    self.tg_client.send_message(tg_user.tg_chat_id, 'Категория не существует')

    def create_goal(self, tg_user, category):
        self.tg_client.send_message(tg_user.tg_chat_id, 'Укажи название задачи. \n'
                                                        'Для отмены введи /cancle')

        response = self.tg_client.get_updates(offset=self.offset)
        for item in response.result:
            self.offset = item.update_id + 1

            if item.message.text == '/cancle':
                continue
            else:
                goal = Goal(title=item.message.text, category=category, user=tg_user.user)
                goal.save()
                self.tg_client.send_message(tg_user.tg_chat_id, f'Создана задача {goal.title}')
