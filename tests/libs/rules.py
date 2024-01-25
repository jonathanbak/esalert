import unittest
from logzero import logger
import sys
import json
import os
import re

currentdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname( os.path.dirname(currentdir) )
sys.path.insert(0, parentdir)
# sys.path.insert(0, '..')
from libs.rules import RuleLoader
from libs.alert import AlertMessage

class RuleLoaderTest(unittest.TestCase):

  # def test_load(self):
  #   logger.info(type(RuleLoader))
  #   r = RuleLoader()
  #   logger.info( type( r.load('disk_full.json') ) )
  #   self.assertTrue( type( r.load('disk_full.json') ) == dict )

  def test_find_values(self):

    r = RuleLoader()
    r.load('response_test_web_firewall.json')
    for k in r.config().all():
      findKeys = r.config().get(k + ".notify_key").split(',')
      resFormat = r.config().get(k + ".notify_format")
      
      newResParams = r.findValues(findKeys)
      print(newResParams)
      notify = AlertMessage(resFormat)
      for o in range(len(newResParams)):
        echoStr = notify.getMessage(*newResParams[o])
        logger.info( echoStr )
        self.assertTrue( type( echoStr ) == str )

if __name__ == '__main__':
  unittest.main()