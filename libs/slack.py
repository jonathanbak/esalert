"""
elasticsearch 검색
"""

from logzero import logger
import requests, json

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
        response = requests.post(self.url, headers=self.headers, data=json.dumps(self.message))
        logger.info(response.text)
        return response