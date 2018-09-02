import logging
from queue import Queue
from threading import Thread

from django.conf import settings
from telegram import Bot as TelegramBot
from telegram.ext import Dispatcher, Updater

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Bot:
    def __init__(self, token, url=settings.SITE_DOMAIN):
        self.bot = TelegramBot(token)
        self.dispatcher = None

        if settings.DEBUG:
            self.updater = Updater(token)
            self.dispatcher = self.updater.dispatcher

            self.updater.start_polling()
        else:
            self.update_queue = Queue()
            self.bot.delete_webhook()
            self.bot.set_webhook('{}/{}/{}/'.format(url, 'bot', token))

            self.dispatcher = Dispatcher(self.bot, self.update_queue)

            thread = Thread(target=self.dispatcher.start, name='dispatcher')
            thread.start()

    def register(self, handler):
        handler.register(self.dispatcher)

    def webhook(self, update):
        self.update_queue.put(update)
