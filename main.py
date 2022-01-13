#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

__author__ = "AnsibleMedia"
__version__ = "0.1.0"

from logzero import logger
from libs.slack import SlackMessage
from libs.elastic import ElasticSearch
from libs.rules import RuleLoader
from libs.alert import AlertMessage
from libs.snooze import Snooze
import config

logger.info('start app')

"""
Clustering
"""
def main():
    c = config.configLoader()
    r = RuleLoader()
    es = ElasticSearch(url=c.get("elastic.url"), headers={"Authorization": "ApiKey "+c.get("elastic.ApiKey")})
    s = Snooze()

    for rule_name in r.config().all():
        findKeys = r.config().get(rule_name + ".notify_key").split(',')
        resFormat = r.config().get(rule_name + ".notify_format")
        searchPath = r.config().get(rule_name + ".search_path")
        alertTitle = r.config().get(rule_name + ".notify_title")
        snoozeMinute = r.config().get(rule_name + ".snooze_minute")

        # 찾을 es쿼리 로드
        searchData = r.load(rule_name+'.json')
        # ES서버 es쿼리 전송
        es.search(searchPath, searchData)
        responseJson = es.getResponse()
        # 쿼리 결과 로드
        r.loadJson(responseJson)
        responseHits = responseJson['hits']['hits']

        # alert 전송할 메시지 필터
        newResParams = r.findValues(findKeys)
        logger.info(newResParams)
        notify = AlertMessage(resFormat)
        for o in range(len(newResParams)):
            echoStr = notify.getMessage(*newResParams[o])

            # 재알림 조건에 따른 알람 발송
            s.setAlarmData(
                {"section": rule_name, "msg": echoStr, "data": responseHits[o]})
            if snoozeMinute and int(snoozeMinute) > 0:
                s.setSnoozeMinute(snoozeMinute)

            if s.isVaildData() and s.isSentMsg() == False:
                s.saveSendMsg()
                SlackInstance = SlackMessage(url=c.get("slack.url"), title=alertTitle, msg=echoStr)
                SlackInstance.send()


if __name__ == "__main__":
    main()
    logger.info('loaded complete..')
