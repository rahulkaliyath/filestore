# File Store 

File store is a local key-value storage system which provides operations such as create, read and delete. 

## Features

* `filestore` can be stored and accessed from anywhere in the system
* Can store values upto `1GB` of data
* Keys will be expired after reaching `time-to-live`
* Supports multi-threading on same client process and is `thread-safe`


## Installation

* Make sure you have <span style="font-size:larger;">[python3](https://www.python.org/downloads/) </span> installed in your system
* Clone the repository and cd into `filestore`
    ``` bash 
        git clone https://github.com/rahulkaliyath/filestore.git
        cd filestore 
     ```
* ``` python
    pip install -r requirements.txt
    ```

## Usage

* Include header files to import `filestore`. If not using inside the `filestore` directory set the path for `filestore` accordingly
    ``` python 
    from filestore import FileStore
    ```
* Instantiate an object for `filestore` class
    ``` python
    file_store = FileStore(filepath = 'file-store')
    ```
    **Note: The file path can be specified while instantiating. If no path is given a default path is taken for storage.**

    If an existing file is found, then `filestore` will use that file

## Create
### `file_store.create( key , json_object , ttl=100 )`

  `create()` takes two neccessary parameters, `key` and `value`. Key is used to access the json_object to perform operations. A key must be of type `string` and should have length less than `32 characters`. The second parameter `value` is a **json_object** which cannot be of size more than `16KB`. Third parameter `ttl` defines the `Time-To-Live` property of the key in seconds. Once a key has reached `Time-To-Live` time span or is **expired**, then that key cannot be used for read or delete operations.

  **Note: The ttl is an optional parameter. If not defined, takes default value of 100**

## Read
### `file_store.read( key )`

  `read(key)` takes one neccessary parameters, `key`. If the `key` is found, the corresponding values is returned. If the key is expired, the key cannot be accessed and will be deleted from the `filestore`. If tried to read a key that does not exist in the `filestore`, appropraite error messages will be shown to user.

## Delete
### `file_store.delete( key )`

  `delete(key)` takes one neccessary parameters, `key`. If the `key` is found or is expired then the key will be deleted from the `filestore`. If tried to delete a key that does not exist in the `filestore`, appropraite error messages will be shown to user.

## Testing

`test_store.py` has test cases which checks basic operations of `filestore` with thread and without threads.

Run the following commands to run tests on `filestore`
### ` python3 test_store.py`