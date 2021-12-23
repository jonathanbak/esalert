"""
Load Rule Files
"""

from logzero import logger
import json
from os import path
from . import constant
import configparser
import re

class RuleConfig:
    DEBUG = False
    TESTING = False
    CONFIG_FILE = path.join(constant.BASE_DIR, 'conf/rules.ini')

    def __init__(self) :
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)

    def get(self, key:str) :
        res = self.config
        keyList = key.split('.')
        for k in keyList:
            if k in res:
                res = res[k]
            else:
                res = None
                break

        return res
    def all(self) :
        return self.config.sections()

class RuleLoader:
    DEFAULT_DIR = "rules"
    rulePath = ""

    def __init__(self, ruleDir:str = None) :
        self.rulePath = constant.BASE_DIR + "/" + ( self.DEFAULT_DIR if ruleDir is None else ruleDir ) + "/"

    def loadJson(self, jsonContent):
        self.json_repr = jsonContent

    def load(self, ruleFile:str):
        ruleFile = self.rulePath + ruleFile
        if path.exists(ruleFile) == False :
            raise Exception("RuleFile Not Found.." + ruleFile)
        jsonData = []
        with open(ruleFile) as json_file:
            jsonData = json.load(json_file)

        self.json_repr = jsonData
        return self.json_repr

    def config(self):
        rc = RuleConfig()

        return rc

    def findValues(self, keyList):
        def find_values(id, json_repr):
            resultList = []
            idList = id.split('.')
            # logger.info(id)
            # logger.info(json_repr)
            cnt = 0
            for k in idList:
                cnt=cnt+1
                if k in json_repr:
                    if re.search('^[0-9]+$', k):
                        k = int(k)
                        
                    if type(json_repr[k]) is list:
                        for json_one in json_repr[k]:
                            if len(idList[cnt:]) == 0 :
                                resultList.append(json_repr[k])
                            else:
                                if type(json_one) is dict or type(json_one) is list:
                                    result2 = find_values('.'.join(idList[cnt:]), json_one)
                                else:
                                    result2 = [json_one]
                                if len(result2)>0:
                                    resultList = resultList + result2

                    else:
                        json_repr = json_repr[k]
                        if len(idList[cnt:]) == 0 :
                            resultList.append(json_repr)
            
            return resultList

        resParams = []
        for m in range(len(keyList)):
            resParams.append(find_values(keyList[m], self.json_repr))
        
        newResParams = list(map(list, zip(*resParams)))

        return newResParams