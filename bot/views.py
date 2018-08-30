import telebot

from .apps import BotConfig


def bot(request):
    BotConfig.bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
