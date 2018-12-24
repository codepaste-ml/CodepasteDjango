from django.apps import AppConfig
from django.conf import settings


class OrnobotConfig(AppConfig):
    name = 'ornobot'

    def ready(self):
        from bot.apps import BotConfig
        from bot.bot import Bot
        from ornobot.handlers import Handlers

        bot = Bot(settings.ORNOBOT_TOKEN)
        bot.register(Handlers())
        BotConfig.registry.add_bot(settings.ORNOBOT_TOKEN, bot)
