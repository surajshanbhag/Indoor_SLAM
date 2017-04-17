#!/usr/bin/python
import numpy as np
import cv2,sys
import socket
import struct
import rospy
import roslib
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import time
import yaml



def parse_yaml(filename,cam_info):
    global image_size
    stream = file(filename, 'r')
    calib_data = yaml.load(stream)
    #cam_info = sensor_msgs.msg.CameraInfo()
    cam_info.width = calib_data['image_width']
    cam_info.height = calib_data['image_height']
    cam_info.K = calib_data['camera_matrix']['data']
    cam_info.D = calib_data['distortion_coefficients']['data']
    cam_info.R = calib_data['rectification_matrix']['data']
    cam_info.P = calib_data['projection_matrix']['data']
    cam_info.distortion_model = calib_data['distortion_model']
    cam_info.height=image_size[1]
    cam_info.width=image_size[0]
    #return cam_info


def receiver(filename=['left.yaml','right.yaml'],CLIENT_PORT=(50677,50678)):
    global image_size

    image_size=[640,320]
    CLIENT_IP='10.42.0.1'
    sockets=[]
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sockets.append(sock)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sockets.append(sock)
    sockets[0].bind(('', CLIENT_PORT[0]))
    sockets[1].bind(('', CLIENT_PORT[1]))


    pic=['','']
    temp=[-1,-1]
# ROS stuf

    image_pub=[]
    image_pub.append(rospy.Publisher("/camera/left/image_raw",Image,queue_size=10))
    image_pub.append(rospy.Publisher("/camera/right/image_raw",Image,queue_size=10))
    cameraInfo_pub=[]
    cameraInfo_pub.append(rospy.Publisher("/camera/left/camera_info",CameraInfo,queue_size=10))
    cameraInfo_pub.append(rospy.Publisher("/camera/right/camera_info",CameraInfo,queue_size=10))
    rospy.init_node('camera_streamer',anonymous=True)
    bridge=CvBridge()
    camera_info=[CameraInfo()]*2
    parse_yaml(filename[0],camera_info[0])
    parse_yaml(filename[1],camera_info[1])
    ################################################################################
    while True:
        temp=[-1,-1]
        flag=[0]*2
        data=['','']
        addr=['','']
        seq=['','']
        img=['','']
        res=['','']
        pic=['','']
        for index in xrange(2):
            while True:
                data[index], addr[index] = sockets[index].recvfrom(image_size[0]*image_size[1])
                seq[index]=struct.unpack('I',data[index][0:4])[0]
                try:
                    if (struct.unpack('I',data[index][4:8])[0]==9999):
                        #print str(index)+' broke'
                        break
                except:
                    pass
                if seq[index]-1 > temp[index]:
                    print str(index)+' error'
                    flag[index]=1
                temp[index]=seq[index]
                pic[index]=pic[index]+data[index][4:]

        for index in xrange(2):
            if seq[index] != temp[index]+1:
                flag[index]=1
                print str(index)+ " flag error $!"
            try:
                if flag[index]==0:
                    img[index] = cv2.imdecode(np.asarray(bytearray(pic[index]),dtype=np.uint8), 1)
                    res[index] = cv2.resize(img[index],None,fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
            except:
                print str(index)+ " flag error %@"
                flag[index]=1

        try:
            if flag[0]==0 and flag[1]==0:
                cv2.imshow('left_frame',res[0])
                cv2.imshow('right_frame',res[1])
                rosTime=rospy.Time.from_sec(time.time())
                camera_info[0].header.stamp=rosTime
                camera_info[1].header.stamp=rosTime
                cameraInfo_pub[0].publish(camera_info[0])
                cameraInfo_pub[1].publish(camera_info[1])
                image_pub[0].publish(bridge.cv2_to_imgmsg(img[0], "bgr8"))
                image_pub[1].publish(bridge.cv2_to_imgmsg(img[1], "bgr8"))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break;
        except:
            pass
        pic=['','']

if __name__ == '__main__':
    receiver([sys.argv[1],sys.argv[2]])
