# flopbox
A simplified reconstruction of dropbox which uses HTTP to sync files between a client folder and a webserver.

### Requirements
- [Flask]
- [requests]

### Usage
1. Run the server on a remote hosting service or another machine using a publically accessable IP address:

    ```python server.py```
2. Run the client in a folder you wish to be synced:

    ```python client.py <server address>```
3. Any changes to files in the directory running client.py will be reflected on the server.

### Under Construction
1. A web interface for accessing files on the server is still being developed.


[Flask]:http://flask.pocoo.org/
[requests]: http://docs.python-requests.org/en/latest/#
