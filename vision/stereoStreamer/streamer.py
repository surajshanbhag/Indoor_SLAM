#!/usr/bin/python

import threading
import time
from videoStream import *

exitFlag = 0
global filtered_quality

def wlan_meas():
    global filtered_quality
    while True:
        cmd = subprocess.Popen('iwconfig wlan0', shell=True,stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'Link Quality' in line:
                temp=float(line.split('=')[1].split('/')[0])
                filtered_quality=0.8*filtered_quality+0.2*temp
            #elif 'Not-Associated' in line:
                #print 'No signal'
        time.sleep(0.2)

if __name__ == '__main__':
# Create new threads
    #wlanlock=threading.Lock()
    #thread1 = videoStream(1, "LeftCamera_Stream", '/dev/video0','10.42.0.1',50677,(640,480),wlanlock)
    #thread2 = videoStream(1, "RightCamera_Stream", '/dev/video1','10.42.0.1',50678,(640,480),wlanlock)
    filtered_quality=55
    image_size=(640,480)
    LeftStreamPort=50677
    RightStreamPort=50678
    if len(sys.argv) > 1:
        client_ip=sys.argv[1]
    else:
        client_ip='10.42.0.1'
    LeftThread=videoStream(1,'Left_Camera','/dev/video0',client_ip,LeftStreamPort,image_size,filtered_quality)
    RightThread=videoStream(2,'Right_Camera','/dev/video1',client_ip,RightStreamPort,image_size,filtered_quality)

    LeftThread.start()
    time.sleep(5)
    #RightCamera_Stream.start()
    while True:
        pass
