import json
import time

import requests


class VkApi:

    URL = "https://api.vk.com/method/{}?access_token={}&{}"

    HEADERS = {
        'Content-type': 'application/json',
        'Cache-control': 'no-cache'
    }

    def __init__(self, token):
        self.token = token
        self.request_lock = -1

    def request(self, method, **kwargs):
        if time.time() - self.request_lock < 1:
            time.sleep(1)

        kwargs.update({'v': '5.92'})
        try:
            params = '&'.join(["{}={}".format(key, value) for key, value in kwargs.items()])
            r = requests.get(
                VkApi.URL.format(method, self.token, params),
                headers=VkApi.HEADERS
            )
            self.request_lock = time.time()
            result = json.loads(r.text)

            return None if 'error' in result else result['response']
        except Exception as e:
            print(e)
        return None

    def get_posts(self, group, request_count=50):
        res = self.request('wall.get', owner_id=-int(group.id), count=request_count, filter='owner')
        result = []
        if res is not None:
            result = [post for post in res['items']]
        return self.filter(group, result)

    def filter(self, group, posts):
        result = []
        for post in posts:
            if group.last_post == post['id']:
                break

            skip = False
            skip |= post.get('marked_as_ads') == 1
            skip |= post.get('is_pinned') == 1
            if not skip:
                result.append(post)

        return result

    def get_video(self, videos):
        res = self.request("video.get", videos=videos)

        if res is not None:
            video_url = None
            if 'files' in res['items'][0]:
                for file, url in res['items'][0]['files'].items:
                    if file != 'external':
                        video_url = url

                return video_url

        return None
