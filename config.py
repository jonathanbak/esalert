import os
import configparser
import libs.constant as constant

# 각종설정
class Config:
    DEBUG = False
    TESTING = False
    CONFIG_FILE = os.path.join(constant.BASE_DIR, 'conf/config.ini')

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

def configLoader() :
    ConfigInstance = Config()
    return ConfigInstance