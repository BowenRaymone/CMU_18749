# Single-server multiple-client TCP chat server

## Introduction
Implementation of a single-server multiple-client TCP/IP chat server for the 18-749 (Building Reliable Distributed Systems) project. Operation is as simple as can be: users connect to the server with a client name and message. 

## Table of contents
<!--ts-->
   * [Dependencies](#dependencies)
   * [Running the code](#running)
   * [Done Done](#donedone)
   * [TODO](#todo)
<!--te-->

<a name="dependencies"></a>
## Dependencies
```
Python 3
```

<a name="running"></a>
## Running the code
- Start up the server:
```
python3 ./src/server.py
```
- Start up the client(s):
```
python3 ./src/client.py -c <CLIENT_NAME> -m <MESSAGE_ID>
```

The port may be specified using ```-p <PORT NUMBER>``` on both client and server. The default port is 10000.

<a name="donedone"></a>
## Done Done
- Simple sever-client app that passes client name and message ID to server
- Server contains a local state counter variable for each connection

<a name="todo"></a>
## TODO
- Too many...

<a name="references"></a>
## References
- https://github.com/tongerlee/18749-project
- https://github.com/18749-Team-7