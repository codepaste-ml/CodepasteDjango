from datetime import datetime

from django.db import models

from pastebot.models import BotUser


class Paste(models.Model):
    class Meta:
        db_table = 'paste_source'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    alias = models.CharField(
        max_length=8,
        verbose_name='Alias',
    )
    language = models.CharField(
        max_length=255,
        verbose_name='Source language',
    )
    created_using_bot = models.BooleanField(
        default=False,
        verbose_name='Is created using telegram bot bot',
    )
    author = models.ForeignKey(
        BotUser,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Telegram bot user'
    )
    creation_date = models.DateTimeField(
        default=datetime.now,
        verbose_name='Creation date'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name',
    )
    source = models.TextField(
        verbose_name='Source',
    )

    def __str__(self):
        return self.name


class Language(models.Model):
    class Meta:
        db_table = 'paste_lang'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    id = models.CharField(
        primary_key=True,
        max_length=255,
        verbose_name='Id',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Text',
    )

    def __str__(self):
        return self.name
