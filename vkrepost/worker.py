import logging
import time

from telegram import InputMediaVideo, InputMediaAnimation, InputMediaPhoto

from vkrepost.models import VkGroup

logger = logging.getLogger(__name__)


class Worker:

    def __init__(self, bot, vkapi):
        self.bot = bot
        self.vkapi = vkapi

    def update(self):
        logger.info('Performing update')
        groups = VkGroup.objects.all()
        for group in groups:
            self.update_group(group)

    def update_group(self, group):
        logger.info('Updating group %s', group.telegram_username)

        posts = self.vkapi.get_posts(group)

        if len(posts) > 0:
            group.last_post = posts[0]['id']
            group.save()

        for post in posts[::-1]:
            logger.info('Processing post with id %s', post['id'])
            self.process_post(post, group)
            time.sleep(1)

    def process_post(self, post, group):
        chat_id = group.telegram_username
        bot = self.bot.bot

        text = post['text']

        photos = []
        gifs = []
        videos = []
        original_order = []
        audios = []

        if 'attachments' in post:
            for attachment in post['attachments']:
                type = attachment['type']
                value = attachment[type]

                if type == 'photo':
                    value = self.get_biggest_photo_size(value)
                    photos.append(value)
                    original_order.append(InputMediaPhoto(value))
                elif type == 'doc' and value['ext'] == 'gif':
                    gif = (value['url'], int(value['size']))
                    gifs.append(gif)
                    original_order.append(InputMediaAnimation(gif))
                elif type == 'video':
                    video_id = '{}_{}'.format(value['owner_id'], value['vid'])
                    video_url = self.vkapi.get_video(video_id)
                    if video_url is not None:
                        videos.append(video_url)
                        original_order.append(InputMediaVideo(video_url))
                elif type == 'audio':
                    audios.append((value['url'], value['artist'] + ' - ' + value['title']))

        has_attachments = len(original_order) > 0
        has_groups = len(original_order) > 1

        if not has_attachments:
            bot.send_message(chat_id, text, parse_mode='HTML')
        elif has_groups:
            bot.send_message(chat_id, text, parse_mode='HTML')
            for i in range(0, len(original_order), 10):
                bot.send_media_group(chat_id, original_order[i:i+10])
        else:
            for photo in photos:
                if len(text) < 200:
                    bot.send_photo(chat_id, photo, caption=text)
                else:
                    text = '<a href="{}">&#8203;</a>{}'.format(photo, text)
                    bot.send_message(chat_id, text, parse_mode='HTML')

            for gif, size in gifs:
                if len(text) >= 200 or size >= 20 * (2 ** 20):
                    text = '<a href="{}">&#8203;</a>{}'.format(gif, text)
                    bot.send_message(chat_id, text, parse_mode='HTML')
                else:
                    bot.send_document(chat_id, gif, caption=text)

            for video in videos:
                if len(text) < 200:
                    bot.send_video(chat_id, video, caption=text)
                else:
                    text = '<a href="{}">&#8203;</a>{}'.format(video, text)
                    bot.send_message(chat_id, text, parse_mode='HTML')

        for audio, caption in audios:
            bot.send_audio(chat_id, audio, caption=caption)

    def get_biggest_photo_size(self, photo):
        sizes = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'])
        return sizes[-1]['url']
