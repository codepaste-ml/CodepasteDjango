from django.apps import AppConfig
from django.conf import settings


class PastebotConfig(AppConfig):
    name = 'pastebot'

    def ready(self):
        from bot.apps import BotConfig
        from bot.bot import Bot
        from pastebot.handlers import Handlers

        bot = Bot(settings.PASTEBOT_TOKEN)
        bot.register(Handlers())
        BotConfig.registry.add_bot(settings.PASTEBOT_TOKEN, bot)
