"""
elasticsearch 검색
"""

from logzero import logger
import requests, json

class ElasticSearch: # 클래스 선언
    url = None
    headers = None
    data = []
    response = None

    def __init__(self, **kwargs) :
        self.url = "" if "url" not in kwargs else kwargs['url']
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        if "headers" in kwargs :
            headers = {**headers, **kwargs['headers']}
        self.headers = headers
        self.data = [] if "data" not in kwargs else kwargs['data']

    def search(self, url:str, data = None):
        data = self.data if data is None else data
        self.response = requests.get(self.url + url, headers=self.headers, data=json.dumps(data),verify=False)

    def getResponse(self):
        # jsonResonse = [] if self.response is None else self.response.json()
        # resCount = jsonResonse['hits']['total']['value']
        # for var in getVarList:
        #     for k in var.split('.'):
        #         jsonResonse.append()
        return [] if self.response is None else self.response.json()