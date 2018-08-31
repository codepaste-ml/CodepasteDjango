import hashlib

from django.conf import settings
from django.db import Error

from paste.models import Source


def start_or_help(bot, update):
    text = 'Send something to get link on this. /records - view your posts'

    update.message.reply_text(text)


def records(bot, update):
    sources = Source.objects.all().filter(
        source_telegram=update.message.from_user.id
    )

    text = 'Your records list:\n'
    for source in sources:
        text += prepare_source_link(source.source_alias) + '\n'

    update.message.reply_text(text)


def paste(bot, update):
    _source = Source(
        source_source=update.message.text,
        source_name='Untitled',
        source_lang='auto',
        source_telegram=update.message.from_user.id,
        source_bot=True
    )

    try:
        _source.save()

        _source.source_alias = hashlib.md5(str(_source.id).encode()).hexdigest()[:8]
        _source.save()

        text = prepare_source_link(_source.source_alias)
        update.message.reply_text(text)
    except Error:
        text = "НАПОМНИТЕ ЭТОМУ СЛАВЕ-ДАУНУ ДОПИСАТЬ ЭТОТ МУСОР"
        update.message.reply_text(text)


def prepare_source_link(alias):
    return '{}/{}'.format(settings.SITE_DOMAIN, alias)
