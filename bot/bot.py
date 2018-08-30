from queue import Queue
from threading import Thread

from telegram import Bot as TelegramBot
from telegram.ext import Dispatcher, CommandHandler, Filters, MessageHandler

from django.conf import settings

from .handlers import start_or_help, records, paste


class Bot:
    def __init__(self, token, url=settings.SITE_DOMAIN):
        self.bot = TelegramBot(token)

        self.bot.delete_webhook()
        self.bot.set_webhook('{}/{}/'.format(url, 'bot'))

        self.update_queue = Queue()
        self.dispatcher = Dispatcher(self.bot, self.update_queue)

        self.register_handlers()
        self.start()

    def register_handlers(self):
        self.dispatcher.add_handler(CommandHandler('start', start_or_help))
        self.dispatcher.add_handler(CommandHandler('help', start_or_help))

        self.dispatcher.add_handler(CommandHandler('records', records))

        self.dispatcher.add_handler(MessageHandler(Filters.text, paste))

    def start(self):
        thread = Thread(target=self.dispatcher.start, name='dispatcher')
        thread.start()

    def webhook(self, update):
        self.update_queue.put(update)
