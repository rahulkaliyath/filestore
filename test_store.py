import unittest
import filestore
import os
import time
import threading
from utils import test_utils
import queue

class TestFileStore(unittest.TestCase):
    def setUp(self):
        self.file_store = filestore.FileStore()

    def test_file_store_created(self):
        output = os.path.exists(self.file_store.filepath)
        self.assertTrue(output)

    def test_create_data(self):
        data = test_utils.data
        data_2 = test_utils.data_2
        output = self.file_store.create("test",data,5)
        self.assertTrue(output)
        output = self.file_store.create("tester",data_2,50)
        self.assertTrue(output)

    def test_create_data_existing_key(self):
        time.sleep(0.5)
        data = test_utils.data
        output = self.file_store.create("test",data,5)
        self.assertFalse(output)

    def test_read_data(self):
        data = test_utils.data
        output = self.file_store.read("test")
        self.assertDictEqual(output,data)

    def test_read_data_after_ttl(self):
        time.sleep(6)
        output = self.file_store.read("test")
        self.assertDictEqual(output,{})

    def test_delete_data(self):
        output = self.file_store.delete("tester")
        self.assertTrue(output)

    def test_delete_deleted_key(self):
        time.sleep(1)
        output = self.file_store.delete("tester")
        self.assertFalse(output)



class TestMultiThreadedFileStore(unittest.TestCase):

    def setUp(self):
        self.file_store = filestore.FileStore()
        self.queue = queue.Queue()
        
    def test_create_with_thread(self):
        data = test_utils.data
        t1 =threading.Thread(target = test_utils.create_data, args=(self.file_store,'test-thread',data,20,self.queue))
        t1.start()
        t1.join()
        self.assertTrue(self.queue.get())

    def test_create_data_race_condition(self):
        data = test_utils.data
        data_2 = test_utils.data_2 
        t1 =threading.Thread(target = test_utils.create_data, args=(self.file_store,'test',data,20,self.queue))
        t2 =threading.Thread(target = test_utils.create_data, args=(self.file_store,'test',data,20,self.queue))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertTrue(self.queue.get())
        self.assertFalse(self.queue.get())

    def test_read_data_on_thread(self):
        data = test_utils.data
        t1 =threading.Thread(target = test_utils.read_data, args=(self.file_store,'test-thread',self.queue))
        t2 =threading.Thread(target = test_utils.read_data, args=(self.file_store,'test-thread',self.queue))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertDictEqual(self.queue.get(),data)
        self.assertDictEqual(self.queue.get(),data)

    def test_delete_data_race_condition(self):
        time.sleep(0.5)
        t1 =threading.Thread(target = test_utils.delete, args=(self.file_store,'test',self.queue))
        t2 =threading.Thread(target = test_utils.delete, args=(self.file_store,'test',self.queue))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertTrue(self.queue.get())
        self.assertFalse(self.queue.get())

if __name__ == '__main__': 
    unittest.main() 