from uuid import uuid4

from telegram import InlineQueryResultCachedVoice
from telegram.ext import InlineQueryHandler


class Handlers:

    AUDIO_DADADA = 'AwADAgADegEAApu8aEg9corkhsv9CwI'
    AUDIO_AAAAAA = 'CQADAgADkgIAAtvbCUmgBARns6QljgI'

    def register(self, dispatcher):
        dispatcher.add_handler(InlineQueryHandler(self.inlinequery))

    def inlinequery(self, bot, update):
        results = [
            InlineQueryResultCachedVoice(
                id=uuid4(),
                voice_file_id=Handlers.AUDIO_DADADA,
                title='Dadadadadadadadadada'
            ),
            InlineQueryResultCachedVoice(
                id=uuid4(),
                voice_file_id=Handlers.AUDIO_AAAAAA,
                title='AAAAAAAAAAAAAAAAAAAA'
            ),
        ]

        update.inline_query.answer(results)
