#!/usr/bin/python
import socket
import sys

def initSocket():
    s=socket.socket()
    print "Created Socket"
    return s

def connect(s, host, port):
   s.connect((host,port))

if __name__ == "__main__":
   s = initSocket()
   s.connect((sys.argv[1],int(sys.argv[2])))
   while True:
       print(s.recv(4096))
       s.send("OK")
       s.recv(4096)
