from django.db import models


class VkGroup(models.Model):
    class Meta:
        db_table = 'vk_group'
        verbose_name = 'VkGroup'
        verbose_name_plural = 'VkGroups'

    telegram_username = models.CharField(
        primary_key=True,
        unique=True,
        verbose_name='Telegram channel name',
        max_length=255
    )

    id = models.IntegerField(
        verbose_name='Vk group id'
    )

    last_post = models.IntegerField(
        default=-1,
        verbose_name='Id of the last post'
    )
