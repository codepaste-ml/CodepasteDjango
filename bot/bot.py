from queue import Queue
from threading import Thread

from django.conf import settings
from telegram import Bot as TelegramBot
from telegram.ext import Dispatcher, CommandHandler, Filters, MessageHandler, Updater

from .handlers import start_or_help, records, paste


class Bot:
    def __init__(self, token, url=settings.SITE_DOMAIN):
        self.bot = TelegramBot(token)
        self.dispatcher = None

        if settings.DEBUG:
            self.updater = Updater(token)
            self.dispatcher = self.updater.dispatcher
            self.register_handlers()

            self.updater.start_polling()
        else:
            self.update_queue = Queue()
            # TODO: token in webhook url
            self.bot.delete_webhook()
            self.bot.set_webhook('{}/{}/'.format(url, 'bot'))

            self.dispatcher = Dispatcher(self.bot, self.update_queue)

            self.register_handlers()

            thread = Thread(target=self.dispatcher.start, name='dispatcher')
            thread.start()

    def register_handlers(self):
        self.dispatcher.add_handler(CommandHandler(['start', 'help'], start_or_help))
        self.dispatcher.add_handler(CommandHandler('records', records))
        self.dispatcher.add_handler(MessageHandler(Filters.text, paste))

    def webhook(self, update):
        self.update_queue.put(update)
