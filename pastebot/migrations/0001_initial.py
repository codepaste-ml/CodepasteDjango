# Generated by Django 2.2.6 on 2019-10-26 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_user_telegram_id', models.IntegerField(unique=True, verbose_name='Telegram user id')),
                ('bot_user_telegram_username', models.CharField(max_length=255, verbose_name='Telegram user name')),
                ('bot_user_admin', models.BooleanField(default=False, verbose_name='Admin')),
                ('bot_user_state', models.CharField(max_length=255, verbose_name='User state')),
                ('bot_user_print_raw', models.BooleanField(default=False, verbose_name='Print raw links')),
            ],
            options={
                'verbose_name': 'BotUser',
                'verbose_name_plural': 'BotUsers',
                'db_table': 'bot_user',
            },
        ),
    ]
