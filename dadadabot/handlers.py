from uuid import uuid4

from django.conf import settings
from telegram import InlineQueryResultCachedVoice
from telegram.ext import InlineQueryHandler


class Handlers:

    def register(self, dispatcher):
        dispatcher.add_handler(InlineQueryHandler(self.inlinequery))

    def inlinequery(self, bot, update):
        results = [
            InlineQueryResultCachedVoice(
                id=uuid4(),
                voice_file_id=settings.DADADABOT_AUDIO,
                title='Dadadadadadadadadada'
            ),
        ]

        update.inline_query.answer(results)
