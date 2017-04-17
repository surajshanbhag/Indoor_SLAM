#!/usr/bin/bash
import numpy as np
import cv2,sys
import rospy
import roslib
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from sensor_msgs.msg import CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import time
import yaml
global camera_info_left
global camera_info_right
global camera_raw_left
global camera_raw_right

def camInfo_left(data):
    global camera_info_left
    camera_info_left=data

def camInfo_right(data):
    global camera_info_right
    camera_info_right=data

def camRaw_left(data):
    global camera_raw_left
    camera_raw_left=data

def camRaw_right(data):
    global camera_info_left
    global camera_info_right
    global camera_raw_left
    global camera_raw_right
    global camerainfo_left_pub,camerainfo_right_pub
    global cameraraw_left_pub,cameraraw_right_pub
    camera_raw_right=data
    rosTime=rospy.Time.from_sec(time.time())
    camera_raw_left.header.stamp=rosTime
    camera_raw_right.header.stamp=rosTime
    camera_info_left.header.stamp=rosTime
    camera_info_right.header.stamp=rosTime
    camera_raw_left.header.frame_id='camera_left_link'
    camera_raw_right.header.frame_id='camera_right_link'
    camera_info_right.header.frame_id='camera_left_link'
    camera_info_right.header.frame_id='camera_right_link'
    cameraraw_left_pub.publish(camera_raw_left)
    cameraraw_right_pub.publish(camera_raw_right)
    camerainfo_left_pub.publish(camera_info_left)
    camerainfo_right_pub.publish(camera_info_right)

if __name__ == '__main__':
    global camerainfo_left_pub,camerainfo_right_pub
    global cameraraw_left_pub,cameraraw_right_pub
    rospy.init_node('camera_sync',anonymous=True)

    rospy.Subscriber('/camera/left/image_raw',Image,camRaw_left)
    rospy.Subscriber('/camera/right/image_raw',Image,camRaw_right)
    rospy.Subscriber('/camera/left/camera_info',CameraInfo,camInfo_left)
    rospy.Subscriber('/camera/right/camera_info',CameraInfo,camInfo_right)

    camerainfo_left_pub=rospy.Publisher('/stereo/left/camera_info',CameraInfo,queue_size=10)
    camerainfo_right_pub=rospy.Publisher('/stereo/right/camera_info',CameraInfo,queue_size=10)
    cameraraw_left_pub=rospy.Publisher('/stereo/left/image_raw',Image,queue_size=10)
    cameraraw_right_pub=rospy.Publisher('/stereo/right/image_raw',Image,queue_size=10)

    rospy.spin()
