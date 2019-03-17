import logging

from django.conf import settings
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class VkRepostConfig(AppConfig):
    name = 'vkrepost'

    def ready(self):
        from bot_adapter.apps import BotConfig
        from bot_adapter.bot import Bot
        from vkrepost.handlers import Handlers
        from vkrepost.vkapi import VkApi
        from vkrepost.worker import Worker

        vkapi = VkApi(settings.VKREPOST_VK_TOKEN)
        bot = Bot(settings.VKREPOST_TOKEN)

        worker = Worker(bot, vkapi)
        bot.register(Handlers(worker))

        BotConfig.registry.add_bot(settings.VKREPOST_TOKEN, bot)
