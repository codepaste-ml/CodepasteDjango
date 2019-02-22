import logging

from django.db import Error
from telegram import ChatAction
from telegram.ext import CommandHandler, MessageHandler, Filters

from vkrepost.models import VkGroup

logger = logging.getLogger(__name__)


class Handlers:

    def __init__(self, worker):
        self.worker = worker

    def register(self, dispatcher):
        user_filter = Filters.chat(username='DarkKeks')
        dispatcher.add_handler(CommandHandler(['add'], self.add_command, user_filter, pass_args=True))
        dispatcher.add_handler(CommandHandler(['list'], self.list_command, user_filter, pass_args=True))
        dispatcher.add_handler(CommandHandler(['reset'], self.reset_command, user_filter, pass_args=True))
        dispatcher.add_handler(CommandHandler(['remove'], self.remove_command, user_filter, pass_args=True))
        dispatcher.add_handler(CommandHandler(['forceupdate'], self.forceupdate_command, user_filter, pass_args=True))
        dispatcher.add_handler(MessageHandler(Filters.all, self.fallback))

    def add_command(self, bot, update, args):
        if len(args) < 2:
            update.message.reply_text('Please specify channel name and vk group id \n'
                                      '/add @example 2281337')
        elif args[0][0] != '@':
            update.message.reply_text(f'{args[0]} is not a valid telegram username')
        elif VkGroup.objects.filter(telegram_username=args[0]).exists():
            update.message.reply_text(f'Group with telegram username {args[0]} already exists')
        else:
            logging.info(f'Adding group id {args[1]} as channel {args[0]}')
            bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

            vk_group = VkGroup(
                telegram_username=args[0],
                id=args[1]
            )

            try:
                vk_group.save()
                update.message.reply_text(f"Added group {args[0]}")
            except Error:
                update.message.reply_text('Something went wrong :(')

    def list_command(self, bot, update, args):
        update.message.reply_text('\n'.join([f"{group.telegram_username} - vk.com/public{group.id}"
                                             for group in VkGroup.objects.all()]))

    def reset_command(self, bot, update, args):
        if len(args) < 1:
            update.message.reply_text('Specify channel name to reset')
        elif not VkGroup.objects.filter(telegram_username=args[0]).exists():
            update.message.reply_text(f'Can\'t find channel with name {args[0]}')
        else:
            logging.info(f'Resetting last post for group {args[0]}')
            try:
                vk_group = VkGroup.objects.get(telegram_username=args[0])
                vk_group.last_post = -1
                vk_group.save()
                update.message.reply_text('Reset last post')
            except Error:
                update.message.reply_text('Something went wrong :(')

    def remove_command(self, bot, update, args):
        if len(args) < 1:
            update.message.reply_text('Specify channel to remove')
        elif not VkGroup.objects.filter(telegram_username=args[0]).exists():
            update.message.reply_text(f'Can\'t find channel with name {args[0]}')
        else:
            update.message.reply_text('Removing')
            vk_group = VkGroup.objects.get(telegram_username=args[0])
            vk_group.delete()

    def forceupdate_command(self, bot, update, args):
        update.message.reply_text('Performing an update')
        logger.info('Force updating')
        self.worker.update()

    def fallback(self, bot, update):
        if update.message:
            update.message.reply_text('Бот для постинга из vk. @darkkeks')
