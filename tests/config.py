import unittest
from logzero import logger
import sys
import os

TEST_DIR = os.path.abspath(os.path.dirname(__file__))

currentdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
# sys.path.insert(0, '..')
import config

class ConfigTest(unittest.TestCase):

    def test_load(self):
        c = config.configLoader()
        logger.info( type( c.get("elastic.ApiKey") ) == str )
        # self.assertTrue( type( c.get("elastic.ApiKey") ) == str )
        self.assertTrue( c.get("elastic.ApiKey") == "asdfasfd" )

if __name__ == '__main__':
    unittest.main()