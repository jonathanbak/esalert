"""
elasticsearch 검색
"""

from logzero import logger
import requests, json
import urllib
import base64
class SlackMessage:
    url = None
    headers = None
    message = ""

    def __init__(self, **kwargs) :
        self.url = None if "url" not in kwargs else kwargs['url']
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        if "headers" in kwargs :
            headers = {**headers, **kwargs['headers']}
        self.headers = headers
        title = "" if "title" not in kwargs else kwargs['title']
        msg = "" if "msg" not in kwargs else kwargs['msg']
        self.message = {
                "text": title,
                "attachments": [
                    {
                        "text": msg,
                        "color": "danger"
                    }
                ]
            }
        logger.info(self.message)
        
    def send(self):
        # msssage = urllib.parse.quote(self.message['text'] + "\n" + self.message['attachments'][0]['text'], '')
        message = self.message['text'] + "\n" + self.message['attachments'][0]['text']
        message = base64.b64encode(message.encode('utf-8')).decode('utf-8')
        response = requests.get(self.url + "/" + message ,timeout=5)
        # response = requests.post(self.url, headers=self.headers, data=json.dumps(self.message))
        logger.info(self.url + "/" + message)
        return response