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
from libs.queue import Queue
import config
import sys
import moment
logger.info('start app')

"""
Clustering
"""
def main():
    c = config.configLoader()
    r = RuleLoader()
    es = ElasticSearch(url=c.get("elastic.url"), headers={"Authorization": "ApiKey "+c.get("elastic.ApiKey")})
    s = Snooze()
    q = Queue()
    
    is_send_alarm_time = False # 알림 발송 시간 (09 ~ 18)
    current_hour = int(moment.now().add(hour=0).format("HH"))
    if current_hour > 9 and current_hour < 18:
        is_send_alarm_time = True

    for rule_name in r.config().all():
        findKeys = r.config().get(rule_name + ".notify_key").split(',')
        resFormat = r.config().get(rule_name + ".notify_format")
        searchPath = r.config().get(rule_name + ".search_path")
        alertTitle = r.config().get(rule_name + ".notify_title")
        snoozeMinute = r.config().get(rule_name + ".snooze_minute")
        slackUrl = r.config().get(rule_name + ".slack_url")
        if slackUrl is None :
            slackUrl = c.get("slack.url")

        # 찾을 es쿼리 로드
        searchData = r.load(rule_name + '.json')
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
        
        if len(newResParams) < 1:
            # print('최근 알림 데이터 삭제', rule_name)
            s.removeLatestSendMsg(rule_name)
        
        for o in range(len(newResParams)):
            echoStr = notify.getMessage(*newResParams[o])

            # 재알림 조건에 따른 알람 발송
            s.setAlarmData(
                {"section": rule_name, "msg": echoStr, "data": responseHits[o]})
            if snoozeMinute and int(snoozeMinute) > 0:
                s.setSnoozeMinute(snoozeMinute)

            if s.isVaildData() and s.isSentMsg() == False:
                
                # 알림발송 시간일때 발송, 아닐경우 큐에 저장
                if is_send_alarm_time:
                    s.saveSendMsg()
                    SlackInstance = SlackMessage(url=slackUrl, title=alertTitle, msg=echoStr)
                    SlackInstance.send()
                else:
                    if rule_name != 'disk_full':
                        q.add_queue({
                            "title": alertTitle,
                            "msg": echoStr
                        })
    
    # 큐에 저장된 알림 발송
    if is_send_alarm_time:
        queue_list = q.get_queue_list()
        if len(queue_list) > 0:
            for i in queue_list:
                SlackInstance = SlackMessage(url=slackUrl, title=i['title'], msg=i['msg'])
                SlackInstance.send()
            q.reset_queue()
        
                            


if __name__ == "__main__":
    main()
    logger.info('loaded complete..')
