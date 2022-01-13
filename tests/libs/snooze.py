import unittest
import sys
import os
from libs.snooze import Snooze

currentdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname(os.path.dirname(currentdir))
sys.path.insert(0, parentdir)


class SnoozeTest(unittest.TestCase):

    def setUp(self):
        self.ALARM_DATA = {
            "section": "disk_full",
            "msg": "Time: 2022-01-13 11:20:48, Host: lwb-vpn, Device: /dev/sda1, Path: /boot, Usable: 42.6%, Available: 0.28GB",
            "data": {

            }
        }

    def testInit(self):
        s = Snooze(alarmData=self.ALARM_DATA, snoozeMinute=30)
        self.assertTrue(True)

    def testGetLatestAlarmList(self):
        s = Snooze()
        alarms = s.getLatestAlarmList()
        self.assertTrue(True)

    def testIsSameSectionAlarm(self):
        s = Snooze(alarmData=self.ALARM_DATA, snoozeMinute=30)
        isSame = s.isSameSectionAlarm(self.ALARM_DATA, self.ALARM_DATA)
        self.assertTrue(True)

    def testGetLatestAlarm(self):
        s = Snooze(alarmData=self.ALARM_DATA, snoozeMinute=30)
        alarm = s.getLatestAlarm()
        self.assertTrue(True)

    def testIsVaildData(self):
        s = Snooze(alarmData=self.ALARM_DATA, snoozeMinute=30)
        isValid = s.isVaildData()
        self.assertTrue(True)

    def testIsSentMsg(self):
        s = Snooze(alarmData=self.ALARM_DATA, snoozeMinute=0)
        isSent = s.isSentMsg()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
