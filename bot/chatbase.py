import requests


class ChatBase:
    TRACK_URL = 'https://chatbase-area120.appspot.com/api/message'

    headers = {
        'Content-type': 'application/json',
        'Cache-control': 'no-cache'
    }

    def __init__(self, token, version):
        self.token = token
        self.version = version

    def track(self, message, event='Message'):
        try:
            params = {
                'api_key': self.token,
                'type': 'user',
                'platform': 'Telegram',
                'message': message.text,
                'intent': event,
                'version': self.version,
                'user_id': message.chat.id
            }

            requests.post(
                self.TRACK_URL,
                params=params,
                headers=self.headers
            ).text()
        except:
            pass
