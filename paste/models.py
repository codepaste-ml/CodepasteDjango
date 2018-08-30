from datetime import datetime

from django.db import models


class Source(models.Model):
    class Meta:
        db_table = 'paste_source'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    source_alias = models.CharField(
        max_length=8,
        verbose_name='Alias',
    )
    source_lang = models.CharField(
        max_length=255,
        verbose_name='Lang',
    )
    source_telegram = models.BooleanField(
        default=False,
        verbose_name='Telegram',
    )
    source_time = models.DateTimeField(
        default=datetime.now(),
        verbose_name='Time'
    )
    source_name = models.CharField(
        max_length=255,
        verbose_name='Name',
    )
    source_source = models.TextField(
        verbose_name='Source',
    )

    def __str__(self):
        return self.source_name


class Lang(models.Model):
    class Meta:
        db_table = 'paste_lang'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    lang_id = models.CharField(
        primary_key=True,
        max_length=255,
        verbose_name='Id',
    )
    lang_text = models.CharField(
        max_length=255,
        verbose_name='Text',
    )

    def __str__(self):
        return self.lang_text
