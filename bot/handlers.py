import hashlib

from django.conf import settings
from django.db import Error
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from bot.models import BotUser
from paste.models import Source

from . lang import translate as _


def prepare_source_link(alias):
    return '{}/{}'.format(settings.SITE_DOMAIN, alias)


class Dialog:

    START = SETTINGS = LIST = None

    _state_by_name = {}

    def __init__(self, name, keyboard):
        self.name = name
        self.method = keyboard
        Dialog._state_by_name[self.name] = self

    def execute(self, callback, **kwargs):
        self.method(callback, **kwargs)

    @staticmethod
    def get(name):
        return Dialog._state_by_name.get(name)

    @staticmethod
    def init():
        Dialog.START = Dialog('start', Dialog.start)
        Dialog.LIST = Dialog('list', Dialog.list)
        Dialog.SETTINGS = Dialog('settings', Dialog.settings)

    @staticmethod
    def start(callback, **kwargs):
        callback(
            text=_('start_message'),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(_('list'), callback_data='list')],
                [InlineKeyboardButton(_('settings'), callback_data='settings')]
            ])
        )

    @staticmethod
    def list(callback, **kwargs):
        callback(
            text=kwargs['text'],
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(_('back'), callback_data='back')
            ]])
        )

    @staticmethod
    def settings(callback, **kwargs):
        callback(
            text=_('settings_text').format(
                _('enabled') if kwargs['print_raw'] else _('disabled')
            ),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(_('print_raw'), callback_data='print_raw')
            ], [
                InlineKeyboardButton(_('back'), callback_data='back')
            ]])
        )


class Handlers:

    def __init__(self, bot):
        self.bot = bot

    def register(self, dispatcher):
        Dialog.init()

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('menu', self.menu))
        dispatcher.add_handler(CommandHandler('list', self.list))
        dispatcher.add_handler(CallbackQueryHandler(self.list, pattern=r'list'))
        dispatcher.add_handler(CallbackQueryHandler(self.settings, pattern=r'settings'))
        dispatcher.add_handler(CallbackQueryHandler(self.raw_toggle, pattern=r'print_raw'))
        dispatcher.add_handler(CallbackQueryHandler(self.back, pattern=r'back'))
        dispatcher.add_handler(MessageHandler(Filters.text | Filters.command, self.paste))

    def start(self, bot, update):
        bot_user = self.get_user(update)
        bot_user.bot_user_state = Dialog.START.name

        Dialog.START.execute(update.message.reply_text)

    def menu(self, bot, update):
        bot_user = self.get_user(update)
        state = Dialog.get(bot_user.bot_user_state)
        state.execute(update.message.reply_text)

    def settings(self, bot, update):
        bot_user = self.get_user(update)
        bot_user.bot_user_state = Dialog.SETTINGS.name
        bot_user.save()

        query = update.callback_query
        query.answer()
        Dialog.SETTINGS.execute(
            query.edit_message_text,
            print_raw=bot_user.bot_user_print_raw
        )

    def list(self, bot, update):
        bot_user = self.get_user(update)
        bot_user.bot_user_state = Dialog.LIST.name
        bot_user.save()

        query = update.callback_query
        query.answer()

        text = _('paste_list')
        sources = Source.objects.all().filter(source_bot_user=bot_user)
        text = text.format('\n'.join([prepare_source_link(source.source_alias) for source in sources]))

        Dialog.LIST.execute(
            query.edit_message_text,
            text=text
        )

    def back(self, bot, update):
        bot_user = self.get_user(update)
        bot_user.bot_user_state = Dialog.START.name
        bot_user.save()

        Dialog.START.execute(update.effective_message.edit_text)

    def raw_toggle(self, bot, update):
        bot_user = self.get_user(update)
        bot_user.bot_user_print_raw = not bot_user.bot_user_print_raw
        bot_user.save()

        self.settings(bot, update)

    def paste(self, bot, update):
        bot_user = self.get_user(update)

        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

        _source = Source(
            source_source=update.message.text,
            source_name='Untitled',
            source_lang='auto',
            source_bot_user=bot_user,
            source_bot=True
        )

        try:
            _source.save()

            _source.source_alias = hashlib.md5(str(_source.id).encode()).hexdigest()[:8]
            _source.save()

            text = _('paste_message').format(prepare_source_link(_source.source_alias))

            update.message.reply_text(text)
        except Error:
            update.message.reply_text(_('something_went_wrong'))

    def get_user(self, update):
        bot_user = BotUser.objects.filter(bot_user_telegram_id=update.effective_user.id)

        if bot_user.count() > 0:
            return bot_user.get()

        bot_user = BotUser(
            bot_user_telegram_id=update.message.from_user.id,
            bot_user_admin=False,
            bot_user_print_raw=False,
            bot_user_state=Dialog.START.name,
            bot_user_telegram_username=update.message.from_user.name
        )

        bot_user.save()
        return bot_user
