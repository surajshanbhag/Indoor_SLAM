#!/usr/bin/python
# first of all import the socket library
import socket

def initialize_Socket():
    # next create a socket object
    s = socket.socket()
    print "Socket successfully created"

    # reserve a port on your computer in our
    # case it is 12345 but it can be anything
    port = 50676

    # Next bind to the port
    # we have not typed any ip in the ip field
    # instead we have inputted an empty string
    # this makes the server listen to requests
    # coming from other computers on the network
    s.bind(('', port))
    print "socket binded to %s" %(port)

    # put the socket into listening mode
    s.listen(5)
    print "socket is listening"
    return s

if __name__ == "__main__":
    s = initialize_Socket();
    c, addr = s.accept()
    reply = "OK"
    while True:
        output = 23
        print 'Got connection from', addr
        if reply == "OK":
            c.send(str(output)+"$");
        if not reply: break
        reply = c.recv(4096)
    print "Test Done"
