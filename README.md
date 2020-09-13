# Single-server multiple-client TCP chat server

## Introduction
Implementation of a single-server multiple-client TCP/IP chat server for the 18-749 (Building Reliable Distributed Systems) project. Operation is as simple as can be: users connect to the server with a username and begin chatting. That's it! 

## Table of contents
<!--ts-->
   * [Dependencies](#dependencies)
   * [Running the code](#running)
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
python3 src/server.py
```
- Start up the client(s):
```
python3 src/client.py -ip <IP ADDRESS> -u <USERNAME>
```

The port may be specified using ```-p <PORT NUMBER>``` on both client and server. The default port is 5000.

<a name="todo"></a>
## TODO
- Colored client-side messages (fancy!)
- Heart beats thread to Replication manager
- Discovery process with Replication manager