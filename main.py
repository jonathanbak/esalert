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
import config

logger.info('start app')

"""
Clustering
"""
def main():
    c = config.configLoader()
    r = RuleLoader()
    es = ElasticSearch(url=c.get("elastic.url"), headers={"Authorization":"ApiKey "+c.get("elastic.ApiKey")} )
    for rule_name in r.config().all():
        findKeys = r.config().get(rule_name + ".notify_key").split(',')
        resFormat = r.config().get(rule_name + ".notify_format")
        searchPath = r.config().get(rule_name + ".search_path")
        alertTitle = r.config().get(rule_name + ".notify_title")
        # 찾을 es쿼리 로드
        searchData = r.load(rule_name+'.json')
        # ES서버 es쿼리 전송
        es.search(searchPath, searchData)
        responseJson = es.getResponse()
        # 쿼리 결과 로드
        r.loadJson(responseJson)

        # alert 전송할 메시지 필터
        newResParams = r.findValues(findKeys)
        logger.info(newResParams)
        notify = AlertMessage(resFormat)
        for o in range(len(newResParams)):
            echoStr = notify.getMessage(*newResParams[o])
            SlackInstance = SlackMessage(url=c.get("slack.url"), title=alertTitle, msg=echoStr )
            SlackInstance.send()

if __name__ == "__main__":
    main()
    logger.info('loaded complete..')