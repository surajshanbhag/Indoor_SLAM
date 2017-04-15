from __future__ import division
import encoder
import socket
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

def left():
    global leftC
    leftC += 1

def checkArgs():
    global IP,host
    if(len(sys.argv)!=1):
        IP = sys.argv[1]
        host = sys.argv[2]

if __name__ == "__main__":
    encoder.encoderSetup()
    checkArgs()
    s = socket.initSocket()
    while True:
        try:
            socket.connect(s,IP,host)
            break
        except:
            pass

    #t1 = threading.Thread(sendData, args= ())
    t = sendData(.01)
    t.daemon = True
    t.start()
    encoder.getEncoder(right,left)
