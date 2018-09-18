from django.apps import AppConfig
from django.conf import settings


class DadadabotConfig(AppConfig):
    name = 'dadadabot'

    def ready(self):
        from bot.apps import BotConfig
        from bot.bot import Bot
        from dadadabot.handlers import Handlers

        bot = Bot(settings.DADADABOT_TOKEN)
        bot.register(Handlers())
        BotConfig.registry.add_bot(settings.DADADABOT_TOKEN, bot)
