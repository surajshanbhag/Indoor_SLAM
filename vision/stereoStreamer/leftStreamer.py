#!/usr/bin/env python
import argparse
import select
import struct
import v4l2capture
import time
import socket
import subprocess
import thread
import sys
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

def streamer(device='/dev/video0',client_ip='10.42.0.1',client_port=50677,image_size=(640,480)):
    global filtered_quality
    filtered_quality=55


    video = v4l2capture.Video_device(device)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    mss=1468
# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
    size_x, size_y = video.set_format(image_size[0],image_size[1], fourcc='MJPG')


# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
    try:
        video.create_buffers(1)
    except:
        print "error : video.create_buffers(1)"
# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
    try:
        video.queue_all_buffers()
    except:
        print "error : video.queue_all_buffers()"
#x=0
# Start the device. This lights the LED if it's a camera that has one.
    try:
        video.start()
    except:
        print "error : video.start()"

    thread.start_new_thread(wlan_meas,())
    while True:
        select.select((video,), (), ())
        try:
            image_data = video.read_and_queue()
            l=len(image_data)
        except IOError:
            print "image_data = video.read_and_queue()"
        i=0
        seq=0
        while i<l:
            sock.sendto(struct.pack('I',seq)+image_data[i:i+mss],(client_ip,client_port))
            i=i+mss
            seq+=1
        sock.sendto(struct.pack('I I',seq,9999),(client_ip,client_port))
        sock.sendto(struct.pack('I I',seq,9999),(client_ip,client_port))
        #print filtered_quality
        if filtered_quality>65:
            spf=0.05
        elif filtered_quality>60:
            spf=0.075
        elif filtered_quality>55:
            spf=0.1
        else:
            spf=0.2
        time.sleep(spf)
    video.close()

if __name__ == '__main__':
    print "USAGE : leftStreamer.py <ip>"
    if len(sys.argv) == 1:
        streamer(client_ip='10.42.0.1')
    else:
        streamer(client_ip=sys.argv[1])
