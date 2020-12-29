from datetime   import datetime ,timedelta
from utils import  helper
from utils.file_handler import *
from values import val
from  threading import Thread, Lock
import time
import json
import pickle
import os
import sys

sys.stdout = open('output.txt', 'w')
lock = Lock()

FILE_PATH = 'file-store'
FILE_NAME = '/store.pickle'
class FileStore:

    def __init__(self, filepath=FILE_PATH):
        self.filepath = filepath + FILE_NAME
        self.store = self.load_store()
        

    def create(self,key,value,ttl=5):
        lock.acquire()
        status = False
        print("[CREATE OPERATION]: Creating New Key '{}'".format(key))
        try :

            if len(key) > 32:
                raise ValueError("Key cannot be of length more than 32 characters") 

            if type(key) != str:
                raise TypeError               

            if key in self.store.keys():
                if helper.is_key_expired(self.store[key]['expiration_time']):
                    del self.store[key]

                    self.commit()
                else:
                    raise ValueError("Key '{}'  already exists".format(key))
            
            if get_file_size(self.filepath,"GB") + get_object_size(value,"GB") >=  1 :
                raise ValueError("FIle Store size reached maximum limit of [1 GB]")
            
            if get_object_size(value,"KB") >16:
                raise ValueError("Value to insert exceeded maximum size limit [16 KB].")

            self.store[key] = {
                'value' :json.dumps(value, indent=4),
                'timestamp': datetime.now(),
                'expiration_time':datetime.now()+timedelta(seconds=ttl)
            }

            self.commit() 
            status = True
            print("[CREATE OPERATION SUCCESS]: Created New Key '{}'".format(key))
        
        except ValueError as err:
            print("[CREATE OPERATION FAILED]: "+str(err))

        except TypeError:
            print("[CREATE OPERATION FAILED]: Key must of type STRING")
        
        except Exception as e:
            print("[CREATE OPERATION FAILED]: "+str(e))
        lock.release()
        return status



    def read(self,key):
        output = {}
        print("[READ OPERATION]: Reading Key '{}'".format(key))
        try:
            if helper.is_key_expired(self.store[key]['expiration_time']):
                lock.acquire()
                del self.store[key]
                self.commit()
                lock.release()
                raise ValueError('Key [{}] Expired'.format(key))         

            else:
                output =  json.loads(self.store[key]['value'])
                print("[READ OPERATION SUCCESS]")

        except KeyError:
            print("[READ OPERATION FAILED]: KEY NOT FOUND. Key might be deleted or expired")
            
        except ValueError as e:
            print("[READ OPERATION FAILED]: "+str(e))
            
        except Exception as e:
            print("[READ OPERATION FAILED]: " +str(e))

        return output
            

    def delete(self,key):
        lock.acquire()
        status = False
        print("[DELETE OPEARATION]: Deleting key '{}'".format(key))
        try:
            del self.store[key]
            self.commit()
            print("[DELETE OPERATION SUCCESS]")
            status =True
        except KeyError:
            print("[DELETE OPERATION FAILED]: KEY NOT FOUND. Key might be deleted or expired")

        except Exception as e:
            print("[DELETE OPERATION FAILED]: "+str(e))
        lock.release()
        return status

          
    def commit(self):
        dump_pickle_file(self.filepath,self.store)
        

    def load_store(self):
        file_store = {}
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath))
            dump_pickle_file(self.filepath,{})
            print("Created a new File Store in '{}'".format(os.path.abspath(self.filepath)))
        else:
            file_store = load_pickle_file(self.filepath)
            print("Accessing Existing File Store from '{}'".format(os.path.abspath(self.filepath)))

        return file_store
