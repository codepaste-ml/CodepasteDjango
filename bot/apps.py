import telebot

from django.apps import AppConfig

from .chatbase import ChatBase


class BotConfig(AppConfig):
    name = 'bot'
    version = '1.0.0'
    site_domain = 'https://codepaste-django.herokuapp.com'
    telegram_bot_token = '430327453:AAFpu-LZHC39yKOmyXTqcErFZmRKWPSSSJ8'
    chatbase_token = '027943b2-d3a0-4bd6-a58f-06c1594ba46f'

    bot = telebot.AsyncTeleBot(telegram_bot_token)
    chatbase = ChatBase(chatbase_token, version)

    bot.remove_webhook()
    bot.set_webhook(url=site_domain + '/bot')
