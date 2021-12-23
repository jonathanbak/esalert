import unittest
from logzero import logger
import sys
import os
currentdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname( os.path.dirname(currentdir) )
sys.path.insert(0, parentdir)
# sys.path.insert(0, '..')
from libs.slack import SlackMessage
import config

class SlackTest(unittest.TestCase):

  def test_send(self):
    c = config.configLoader()
    SlackInstance = SlackMessage(url=c.get("slack.url"), title="Test Msg", msg="message alert" )
    logger.info( SlackInstance.send() )
    self.assertTrue( True )

if __name__ == '__main__':
  unittest.main()