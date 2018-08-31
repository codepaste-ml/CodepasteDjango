from django.db import models


class BotUser(models.Model):
    class Meta:
        db_table = 'bot_user'
        verbose_name = 'BotUser'
        verbose_name_plural = 'BotUsers'

    bot_user_telegram_id = models.IntegerField(
        unique=True,
        verbose_name='Telegram user id'
    )

    bot_user_telegram_username = models.CharField(
        verbose_name='Telegram user name',
        max_length=255
    )

    bot_user_admin = models.BooleanField(
        verbose_name='Admin',
        default=False
    )

    bot_user_state = models.CharField(
        verbose_name='User state',
        max_length=255
    )

    bot_user_print_raw = models.BooleanField(
        verbose_name='Print raw links',
        default=False
    )

    def __str__(self):
        return self.bot_user_telegram_username
