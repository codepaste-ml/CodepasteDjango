from django.apps import AppConfig

from Codepaste import settings
from .bot import Bot


class BotConfig(AppConfig):
    name = 'bot'
    version = '1.0.0'
    telegram_bot_token = settings.TELEGRAM_BOT_TOKEN
    chatbase_token = settings.CHATBASE_TOKEN

    bot = Bot(telegram_bot_token)
