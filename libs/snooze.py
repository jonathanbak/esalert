import sys
import json
import os
from os import path
import math
from . import constant
from datetime import datetime
from libs.rules import RuleLoader


class Snooze:
    LATEST_SEND_FILE = path.join(constant.BASE_DIR, './lastest_alarm.json')
    alarmData = {}
    snoozeMinute = 0

    def __init__(self, **kwargs):
        # print('Snooze __init__')
        self.snoozeMinute = kwargs.get("snoozeMinute", 0)
        self.alarmData = kwargs.get("alarmData", {})

    # 발송할 데이터 설정
    def setAlarmData(self, alarmData):
        self.alarmData = alarmData

    # 재알림 방지 시간 설정
    def setSnoozeMinute(self, snoozeMinute):
        self.snoozeMinute = int(snoozeMinute)

    # 최근 발송 메세지 목록
    def getLatestAlarmList(self):
        alarms = []
        if os.path.isfile(self.LATEST_SEND_FILE) == True:
            with open(self.LATEST_SEND_FILE, encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                for jsonData in json_data:
                    alarms.append(jsonData)

        return alarms

    # 최근에 발송여부
    def isSentMsg(self):

        isSent = False

        is_vaild_data = self.isVaildData()  # 입력값 오류일 경우 발송했다고 반환처리

        if is_vaild_data:

            matchAlarm = self.getLatestAlarm()
            # print('matchAlarm', json.dumps(matchAlarm))
            # print('self.alarmData', json.dumps(self.alarmData))

            isSnoozeAlarm = self.isSnoozeAlarm()

            if matchAlarm:
                send_datetime = datetime.strptime(self.alarmData["data"]["fields"]["timestamp"][0], "%Y-%m-%d %H:%M:%S")
                last_send_datetime = datetime.strptime(matchAlarm["data"]["fields"]["timestamp"][0], "%Y-%m-%d %H:%M:%S")
                
                if json.dumps(matchAlarm) == json.dumps(self.alarmData) or send_datetime < last_send_datetime:
                    isSent = True
                elif isSnoozeAlarm and self.snoozeMinute > 0:
                    isSent = True
        else:
            isSent = True

        return isSent

    # 입력데이터가 정상인지 여부
    def isVaildData(self):
        is_vaild = False
        try:
            timestamp = datetime.strptime(self.alarmData["data"]["fields"]["timestamp"][0], "%Y-%m-%d %H:%M:%S")
            is_vaild = True
        except:
            is_vaild = False
            # print("Doesn't exist")
        return is_vaild

    # 신규로 발송할 알림이 최근 알림 발송 파일에 있는 데이터 경우 반환
    def getLatestAlarm(self):
        alarms = self.getLatestAlarmList()
        matchAlarm = {}
        for jsonData in alarms:
            isSameSection = self.isSameSectionAlarm(jsonData, self.alarmData)
            if isSameSection == True:
                matchAlarm = jsonData
                break

        return matchAlarm

    # 알림 비교 (같은 유형)
    def isSameSectionAlarm(self, source, target):
        isSame = False

        RuleSource = RuleLoader()
        RuleSource.loadJson(source)

        RuleTarget = RuleLoader()
        RuleTarget.loadJson(target)

        if source["section"] == target["section"]:

            findKeys = []
            findKey = RuleSource.config().get(source["section"] + ".snooze_key")
            if findKey:
                findKeys = findKey.split(',')
            sourceValues = RuleSource.findValues(findKeys)
            targetValues = RuleTarget.findValues(findKeys)
            if sourceValues == targetValues:
                isSame = True
        return isSame

    # 알링 비교 (재알림 여부)
    def isSnoozeAlarm(self):

        isSnooze = False
        matchAlarm = self.getLatestAlarm()
        if matchAlarm:

            send_datetime = datetime.strptime(self.alarmData["data"]["fields"]["timestamp"][0], "%Y-%m-%d %H:%M:%S")
            last_send_datetime = datetime.strptime(matchAlarm["data"]["fields"]["timestamp"][0], "%Y-%m-%d %H:%M:%S")

            # print("신규 알림 시간: ", send_datetime)
            # print("최근 알림 시간: ", last_send_datetime)

            if send_datetime > last_send_datetime:
                # 최근 스누즈 설정시간(30분) 이내에 발송된 알림인지 확인
                date_diff = send_datetime - last_send_datetime
                past_minute = date_diff.seconds / 60
                # print("최근 알림후 :", math.ceil(past_minute), '분 지남')
                if self.snoozeMinute > 0 and past_minute < self.snoozeMinute:
                    isSnooze = True

        return isSnooze

    # 알림 파일에 저장
    def saveSendMsg(self):
        # print('알림 메세지 저장')
        isSave = False
        isSent = self.isSentMsg()
        if isSent == False:
            alarms = []
            null = None
            if os.path.isfile(self.LATEST_SEND_FILE) == True:
                with open(self.LATEST_SEND_FILE, encoding="utf-8") as json_file:
                    json_data = json.load(json_file)
                    for jsonData in json_data:
                        isSameSection = self.isSameSectionAlarm(jsonData, self.alarmData)
                        if isSameSection == False:
                            alarms.append(jsonData)
            alarms.append(self.alarmData)
            save_file = open(self.LATEST_SEND_FILE, "w", encoding="utf-8")
            json.dump(alarms, save_file, ensure_ascii=False, indent=4)
            save_file.close()
            isSave = True

        return isSave
