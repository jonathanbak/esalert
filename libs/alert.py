"""
Alert Message Formater
"""

from logzero import logger

class AlertMessage:
    msgFormat = ""

    def __init__(self, msgFormat:str = None) :
        if msgFormat is not None :
            self.msgFormat = msgFormat

    def getMessage(self, *args):
        echoStr = self.msgFormat.format(*args)
        # logger.info(echoStr)
        
        return echoStr