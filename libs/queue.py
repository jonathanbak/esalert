import json
import os
from os import path
from . import constant

class Queue:
    QUEUE_FILE = path.join(constant.BASE_DIR, './alarm_queue.json')

    def __init__(self, **kwargs):
        pass
    
    def add_queue(self, msg):
        queue_list = self.get_queue_list()
        queue_list.append(msg)
        save_file = open(self.QUEUE_FILE, "w", encoding="utf-8")
        json.dump(queue_list, save_file, ensure_ascii=False, indent=4)
        save_file.close()
            
    def get_queue(self):
        queue = False
        if os.path.isfile(self.QUEUE_FILE) == True:
            with open(self.QUEUE_FILE, encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                for jsonData in json_data:
                    queue = jsonData
                    break
        return queue

    def get_queue_list(self):
        queue_list = []
        if os.path.isfile(self.QUEUE_FILE) == True:
            with open(self.QUEUE_FILE, encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                for jsonData in json_data:
                    queue_list.append(jsonData)
        return queue_list
    
    def reset_queue(self):
        queue = []
        save_file = open(self.QUEUE_FILE, "w", encoding="utf-8")
        json.dump(queue, save_file, ensure_ascii=False, indent=4)
        save_file.close()
