from django.conf import settings
from django.apps import AppConfig


class VkRepostConfig(AppConfig):
    name = 'vkrepost'

    def ready(self):
        from bot.apps import BotConfig
        from bot.bot import Bot
        from vkrepost.handlers import Handlers
        from vkrepost.vkapi import VkApi
        from vkrepost.worker import Worker
        from background_task import background

        vkapi = VkApi(settings.VKREPOST_VK_TOKEN)
        bot = Bot(settings.VKREPOST_TOKEN)

        worker = Worker(bot, vkapi)
        bot.register(Handlers(worker))

        BotConfig.registry.add_bot(settings.VKREPOST_TOKEN, bot)

        @background(schedule=10)
        def update_task():
            worker.update()

        update_task(repeat=300)
