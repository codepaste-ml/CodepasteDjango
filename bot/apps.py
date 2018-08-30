from django.apps import AppConfig

from .bot import Bot


class BotConfig(AppConfig):
    name = 'bot'
    version = '1.0.0'
    telegram_bot_token = '430327453:AAFpu-LZHC39yKOmyXTqcErFZmRKWPSSSJ8'
    chatbase_token = '027943b2-d3a0-4bd6-a58f-06c1594ba46f'

    bot = Bot(telegram_bot_token)
