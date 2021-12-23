import unittest
from logzero import logger
import sys
import os
currentdir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.dirname( os.path.dirname(currentdir) )
sys.path.insert(0, parentdir)
# sys.path.insert(0, '..')
from libs.elastic import ElasticSearch
from libs.rules import RuleLoader
from libs.alert import AlertMessage
import config

class ElasticTest(unittest.TestCase):

  def test_load(self):
    c = config.configLoader()
    r = RuleLoader()
    # data = '{  "query":{      "bool": {        "filter": [          {            "match": {              "metricset.name":"filesystem"            }          },          {            "range": {              "@timestamp": {                "gt": "now-1m"              }            }          }        ],         "must": [          {            "range": {              "system.filesystem.used.pct":{                "gte" : 0.85              }            }          }        ]      }    },    "script_fields":{       "timestamp":{            "script":{            "lang": "painless",            "source":"String datetime = params._source[\'@timestamp\'];ZonedDateTime zdt = ZonedDateTime.parse(datetime);DateTimeFormatter dtf = DateTimeFormatter.ofPattern(\"yyyy-MM-dd HH:mm:ss\");String updatedZdt = zdt.plusHours(9).format(dtf);updatedZdt"          }       },       "available":{            "script":{            "lang": "painless",            "source":"float aa = (float)Math.round((float)params._source.system.filesystem.available / 1024 / 1024 / 1024 * 100) / 100; aa + \'GB\'"          }       },       "pct":{            "script":{            "lang": "painless",            "source":"float aa = (float)Math.round((float)params._source.system.filesystem.used.pct * 1000) / 10; aa + \'%\'"          }       }     },    "_source":[       "host.name","system.filesystem.used.pct","system.filesystem.available","system.filesystem.mount_point","system.filesystem.device_name"    ]}'
    es = ElasticSearch(url=c.get("elastic.url"), headers={"Authorization":"ApiKey "+c.get("elastic.ApiKey")} )
    r = RuleLoader()
    for k in r.config().all():
      findKeys = r.config().get(k + ".notify_key").split(',')
      resFormat = r.config().get(k + ".notify_format")
      searchPath = r.config().get(k + ".search_path")
      reqeustData = r.load('disk_full.json')
      es.search(searchPath, reqeustData)
      response = es.getResponse()
      r.loadJson(response)
      newResParams = r.findValues(findKeys)
      logger.info(newResParams)
      notify = AlertMessage(resFormat)
      for o in range(len(newResParams)):
        echoStr = notify.getMessage(*newResParams[o])
        logger.info( echoStr )
        self.assertTrue( type( echoStr ) == str )

    # self.assertTrue( type( response ) == str )

if __name__ == '__main__':
  unittest.main()