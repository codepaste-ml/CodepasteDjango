import hashlib

from django.db import Error

from paste.models import Source
from .apps import BotConfig

bot = BotConfig.bot
chatbase = BotConfig.chatbase


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    text = 'Send something to get link on this. /records - view your posts'

    bot.send_message(message.chat.id, text)
    chatbase.track(message, 'start/help')


@bot.message_handler(commands=['records'])
def records_handler(message):
    sources = Source.objects.all().filter(
        source_telegram=message.chat.id
    )

    text = 'Your records list:\n'
    for source in sources:
        text += '{}/{}\n'.format(BotConfig.site_domain, source.source_alias)

    bot.send_message(message.chat.id, text)
    chatbase.track(message, 'records')


@bot.message_handler(content_types=['text'])
def text_handler(message):
    _source = Source(
        source_source=message.text,
        source_name='Untitled',
        source_lang='auto',
        source_telegram=message.chat.id,
        source_bot=True
    )

    try:
        _source.save()

        _source.source_alias = hashlib.md5(str(_source.id).encode()).hexdigest()[:8]
        _source.save()

        text = prepare_source_link(_source.source_alias)
        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)
    except Error:
        text = "НАПОМНИТЕ ЭТОМУ СЛАВЕ-ДАУНУ ДОПИСАТЬ ЭТОТ МУСОР"
        bot.send_message(message.chat.id, text, reply_to_message_id=message.message_id)

    chatbase.track(message, 'text')


def prepare_source_link(alias):
    return '{}/{}'.format(BotConfig.site_domain, alias)
