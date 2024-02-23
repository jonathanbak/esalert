import unittest
from libs.queue import Queue
import urllib
import base64

class QueueTest(unittest.TestCase):

    def setUp(self):
        pass
    
    def testQueue(self):
        q = Queue()
        
        # queue = q.get_queue()
        # print(queue)
        
        # queue_list = q.get_queue_list()
        # print(queue_list)
                
        # q.reset_queue()
        
        # msssage = urllib.parse.quote('https://m.wendybook.com', '')
        message = 'https://m.wendybook.com'
        msssage = base64.b64encode(message.encode('utf-8')).decode('utf-8')


        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()