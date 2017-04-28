from __future__ import division
import encoder
import socket_class as socket
import threading
import time
import sys

rightC,leftC = (0,0)
s = None
IP = "10.42.0.1"
host = 50679
class sendData(threading.Thread):
    def __init__(self,waitTime):
        self.waitTime = waitTime
        threading.Thread.__init__(self)

    def run(self):
        #send info every waitTime
        global s
        global rightC,leftC
        conf = "OK"
        while True:
            if(conf == "OK"):
                s.send(str(rightC)+","+str(leftC))
                conf = s.recv(10)
                print "sent",str(rightC),",",str(leftC)
                time.sleep(self.waitTime)

def right():
    global rightC
    rightC += 1
    print "right: ",rightC,"\t","left :",leftC

def left():
    global leftC
    leftC += 1
    print "right: ",rightC,"\t","left :",leftC

def checkArgs():
    global IP,host
    if(len(sys.argv)!=1):
        IP = sys.argv[1]
        host = sys.argv[2]

if __name__ == "__main__":
    """if 2 arguments are passed in overwrite IP and port number to those values else use IP = 10.42.0.1 and 50679"""
    encoder.encoderSetup()
    if len(sys.argv) in (1,3):
        checkArgs()
        s = socket.initSocket()
        while True:
            try:
                socket.connect(s,IP,host)
                break
            except:
                pass
        
        #start thread to send info in background
        t = sendData(.01)
        t.daemon = True
        t.start()
        
        #read encoder values
        encoder.getEncoder(right,left)
    else:
        encoder.getEncoder(right,left)

