import time
data = {
    "name" : "test",
    "id" : 1,
    "users": [1,2,3]
}

data_2 = {
    "name" : "tester",
    "id" : 1,
    "users": [1,2,3]
}
def create_data(file_store,key,value,ttl,queue):
    output = file_store.create(key,value,ttl)
    return queue.put(output)

def read_data(file_store,key,queue):
    output = file_store.read(key)
    return queue.put(output)

def delete(file_store,key,queue):
    output = file_store.delete(key)
    return queue.put(output)