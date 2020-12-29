from utils.key_mapping import sizes
import os
import sys
import pickle

def get_file_size(file,size_needed):
    return  os.path.getsize(file) / sizes[size_needed]

def get_object_size(object,size_needed):
    return sys.getsizeof(object) / sizes[size_needed]

def load_pickle_file(filepath):
    with open(filepath, 'rb') as handle:
        return pickle.load(handle)

def dump_pickle_file(filepath,file):
    with open(filepath,'wb') as file_handler:
        pickle.dump(file,file_handler)