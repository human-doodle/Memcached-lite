# Memcached-lite

## Introduction
Designed and implemented a simple key-value store. A server is implemented, that does the job of storing and retrieving data for multiple clients. The server stores a unique value for each key using the set command and retrieves values using the get command. This assignment aims to implement a lite version of the Memcached, which is a popular keyvalue store. Tried to mimic client protocol of Memcached. One difference would be that unlike the Memcached storing the data in memory, our server will be using stable storage, meaning the data will persist even aDer the server process dies.

## Design Details
### Basic Server
The Memcached-lite server was implemented as a TCP-socket server listening on port 9889 for client connections. The server utilizes file system, in my case a JSON file ('cache.json') for keyvalue storage. It maintains a dictionary/map data structure for efficient key-value management and ensure data persistence even after the server process dies.

The server supports the following commands:
```
1. set <key> <value> \r\n : Stores a key-value pair on the server.
2. get <key> \r\n : Retrieves the value associated with a given key.
```
File Structure: I use JSON file structure for this task, since it is a lightweight and straighforward format for key-value data.

#### Set
The set command consists of two lines:
```
set <key> <value-size-bytes> \r\n
<value> \r\n
```
The server responds with either "STORED\r\n" if the data is successfully stored or "NOTSTORED\ r\n" if there is an issue.

The reader of data (either server or client) will always know, from a preceding text line, the exact length of the data block being transmiaed. (<value-size-bytes >) Text lines are always terminated by \r\n. Although unstructured data is also terminated by \r\n, but \r, \n or any other 8-bit characters may also appear inside the data. That’s the reason why when a client retrieves data from a server, it must use the length of the data block (which it will be provided with (value-size-bytes >) to determine where the data block ends, and not the fact that \r\n follows the end of the data block, even though it does.
The server first takes a command line and expects next data block of the size it got in the command line.
Note: since “add” or “replace” commands are not implemented here, “NOT_STORED\r\n” doesn’t mean that the condition for add or replace wasn’t met as in Memcached, but in this scenario, is returned because of an error like wrong command/ invalid (<value-size-bytes >) or absence of <value-size-bytes > in the command.

#### Get
The get command retrieves data as follows:
```
VALUE <key> <bytes> \r\n
<data block>\r\n
END\r\n
```
The server sends "END\r\n" when all items have been transmited. After this command, the client expects an item, each of which is received as text line followed by a data block of the size <bytes>. ADer all the items have been received, the server ends with the string – ‘END\r\n’ to indicate end of response.
In our case since, the server stores unique values for each key, every key will have one unique item. The server returned ‘INVALID’ message in the case of error.

### Clients and Test Cases

Client programs were implemented accordingly to send commands to the server and receiving and displaying the messages from the server. Client was connected to the server and executed a series of get and set requests for testing purposes. Initially 2 clients were used to evaluate the server's concurrent handling of requests. This test was done by introducing sleep in the server for set command for 10 seconds, and running get command from another client concurrently
Following test cases were run:
```
1. Client: set Shivani 5
Rahul
Server output: STORED\r\n
2. Client: get Shivani
Server output:
Rahul
END\r\n
3. Client: set Rahul 4
Shivani
Server output:
STORED\r\n
```
NOTE: here, the size given was 4 but the client provided with 7 characters. The server will only
receive 4 characters, and thus as a result, the rest 3 leaer will not be stored.
```
4. Client: get Rahul
Server output:
Shiv
END\r\n
5. Client: set Rahul shivani
Server output:
NOT_STORED\r\n
```
NOTE: This happened before, the command was invalid, server was expecting a value which
was not provided.
Testing concurrency is shown in the next section
###  Advanced: Concurrency
Concurrency was achieved by allowing the server to handle more than one request at a time. The code spawns a new thread for each client connection, which is a good approach for
handling multiple clients concurrently. By using threads, the server handles multiple client connections simultaneously. 
For each new client connection, a new thread is created using threading.Thread. The handle_client function is wriaen as the target function for the thread where the handle_client
function handles the communication with the individual client in a separate thread, allowing muliple clients to be serviced concurrently without blocking each other. Each client is
processed independently in its thread, ensuring that one client's actions do not block other clients from making requests or receiving responses. To check for concurrency, we run a python script, launching multiple clients concurrently using threading.Thread and python subprogram

Checked with 5, 10, 15 and 20 clients.

### Experimental Evaluation

#### Performance
The server was tested for performance using different numbers of concurrent clients in terms
of response times. The server showed good performance up to a certain level of concurrency
For 5 concurrent clients doing set operations, total execution time was: 0.090 sec
For 10 concurrent clients doing set operations, total execution time was: 0.15 sec
For 15 concurrent clients doing set operations, total execution time was: 0.25 sec
For 20 concurrent clients doing set operations, total execution time was: 0.36 sec
The response time by the server showed good performance up to a certain level of
concurrency, aDer which response times started to degrade.

#### Limitations
Concurrency limits: The server's performance starts to degrade at high levels of concurrency. Data consistency in a multi-threaded server like this is a limitation in this scenario since multiple threads are simultaneously reading from and writing to shared data file – cache.json. There might be situations when multiple threads may aaempt to read and write to the JSON file simultaneously, leading to data corruption or unexpected behavior. For example, if two threads
atempt to update the JSON file at the same time, one may overwrite changes made by the other. Also, reading and writing to the same file from multiple threads can cause synchronization. For example, if one thread is writing to the file while another is reading it, the read operation may yield incomplete or incorrect data. Potential improvements
Data inconsistency issues can be dealt with proper synchronization and resource locking(one thread accessing shared resource at a time).

### Files:
1.  server.py : code for server implementation
2.  client.py: code for client implementation
3. multiple_client_test.py : code for starting multiple clients for concurrent requests to server.
4. cache.json : sample file system for storage and retrieval of key-value(will be created by
server if already doesn’t exist)

## References :
1. haps://github.com/memcached/memcached/blob/master/doc/protocol.txt
2. haps://github.com/memcached/memcached/wiki/Commands#set
3. haps://pymemcache.readthedocs.io/en/latest/gesng_started.html
4. haps://docs.python.org/3/library/socket.html
5. haps://pymotw.com/2/socket/tcp.html
6. haps://docs.python.org/3/library/subprocess.html
