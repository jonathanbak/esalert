import unittest
from libs.queue import Queue

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
        self.assertTrue(True)
        

if __name__ == '__main__':
    unittest.main()
