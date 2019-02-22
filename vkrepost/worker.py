import html
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
            try:
                self.process_post(post, group)
            except Exception as err:
                logger.exception(f"Exception occurred while processing post from "
                                 f"{group.telegram_username} - id {post['id']}", err)
            time.sleep(3)

    def process_post(self, post, group):
        chat_id = group.telegram_username
        bot = self.bot.bot

        text = html.escape(post['text'])

        media_groups = []
        photos = []
        gifs = []
        videos = []
        audios = []

        if 'attachments' in post:
            for attachment in post['attachments']:
                type = attachment['type']
                value = attachment[type]

                if type == 'photo':
                    value = self.get_biggest_photo_size(value)
                    photos.append(value)
                    media_groups.append(InputMediaPhoto(value))
                elif type == 'doc' and value['ext'] == 'gif':
                    gifs.append(value['url'])
                elif type == 'video':
                    video_id = '{}_{}'.format(value['owner_id'], value['id'])
                    video_url = self.vkapi.get_video(video_id)
                    if video_url is not None:
                        videos.append(video_url)
                        media_groups.append(InputMediaVideo(video_url))
                elif type == 'audio':
                    audios.append((value['url'], value['artist'] + ' - ' + value['title']))

        def send_text():
            if text:
                bot.send_message(chat_id, text, parse_mode='HTML')

        has_attachments = len(media_groups) + len(gifs) > 0

        if not has_attachments:
            send_text()
        elif len(media_groups) > 1:
            send_text()

            for i in range(0, len(media_groups), 10):
                bot.send_media_group(chat_id, media_groups[i:i+10])

            for gif in gifs:
                bot.send_animation(chat_id, gif)
        else:
            def send_encoded(attachment, send_specific, send_common):
                if not text or len(text) < 200:
                    send_specific(chat_id, attachment, caption=text, parse_mode='HTML')
                else:
                    send_common(chat_id, self.encode_attachment_url(attachment, text), parse_mode='HTML')

            attachment_count = len(photos) + len(videos) + len(gifs)
            if attachment_count > 1:
                send_text()
                text = None

            for photo in photos:
                send_encoded(photo, bot.send_photo, bot.send_message)
            for video in videos:
                send_encoded(video, bot.send_video, bot.send_message)
            for gif in gifs:
                send_encoded(gif, bot.send_animation, bot.send_message)

        for audio, caption in audios:
            bot.send_audio(chat_id, audio, caption=caption)

    def get_biggest_photo_size(self, photo):
        sizes = sorted(photo['sizes'], key=lambda x: x['width'] * x['height'])
        return sizes[-1]['url']

    def encode_attachment_url(self, url, text):
        return '<a href="{}">&#8203;</a>{}'.format(url, text if text is not None else '')
