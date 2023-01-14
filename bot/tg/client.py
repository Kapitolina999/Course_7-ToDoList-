import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, GET_UPDATES_SCHEMA, SEND_MESSAGE_SCHEMA


class TgClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response = requests.get(self.get_url(f'getUpdates?offset={offset}&timeout={timeout}&'
                                             f'allowed_updates=["update_id","message"]'))
        print(response.json())
        return GET_UPDATES_SCHEMA.load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('sendMessage')
        response = requests.post(url, json={'chat_id': chat_id, 'text': text})
        print(response.json())
        return SEND_MESSAGE_SCHEMA.load(response.json())
