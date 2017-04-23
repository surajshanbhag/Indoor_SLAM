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

def streamer(device,client_ip,client_port,image_size):
    global filtered_quality
    filtered_quality=55
    image_size=[int(value) for value in image_size.split(',')]
    print image_size


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

    parser = argparse.ArgumentParser(description='v4l based streamer')
    parser.add_argument('--device',required=True,default='/dev/video0',help='device name ex: /  dev/video0')
    parser.add_argument('--ip',required=False,default='10.42.0.1',help='client IP to whom video is streamed ')
    parser.add_argument('--port',required=False,default='50677',help='client IP to whom video   is streamed ')
    parser.add_argument('--size',required=False,default='640,480',help='image size to be      streamed')
    args = vars(parser.parse_args())
    print(args)
    streamer(device=args['device'],client_ip=args['ip'],client_port=int(args['port']),image_size=args['size'])
