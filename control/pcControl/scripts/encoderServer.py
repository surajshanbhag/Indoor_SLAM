#!/usr/bin/python

import socket

def initiliaze_Socket():
    s=socket.socket()
    print "Socket created"

    port =50679

    s.bind(('',port))
    print "socket bound to %s" %(port)

    s.listen(5)
    print 'socket is listening'
    return s

if __name__ == '__main__':
    s=initiliaze_Socket()
    c, addr=s.accept()
    print 'got connection from ' , addr
    while True:
        received=c.recv(100)
        c.send('OK')
        print received
    print 'Test Done'
