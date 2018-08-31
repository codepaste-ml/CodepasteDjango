from queue import Queue
from threading import Thread

from django.conf import settings
from telegram import Bot as TelegramBot
from telegram.ext import Dispatcher, Updater

from .handlers import Handlers


import logging
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Bot:
    def __init__(self, token, url=settings.SITE_DOMAIN):
        self.bot = TelegramBot(token)
        self.handler = Handlers(self)
        self.dispatcher = None

        if settings.DEBUG:
            self.updater = Updater(token)
            self.dispatcher = self.updater.dispatcher

            self.handler.register(self.dispatcher)

            self.updater.start_polling()
        else:
            self.update_queue = Queue()
            # TODO: token in webhook url
            self.bot.delete_webhook()
            self.bot.set_webhook('{}/{}/'.format(url, 'bot'))

            self.dispatcher = Dispatcher(self.bot, self.update_queue)

            self.handler.register(self.dispatcher)

            thread = Thread(target=self.dispatcher.start, name='dispatcher')
            thread.start()

    def webhook(self, update):
        self.update_queue.put(update)
