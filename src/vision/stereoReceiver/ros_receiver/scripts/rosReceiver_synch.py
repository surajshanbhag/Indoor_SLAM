#!/usr/bin/bash
import argparse
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

    # sample topics in each callback and when the right image topic is received publish all
    # at once with new timestamps

    rosTime=rospy.Time.from_sec(time.time())
    camera_raw_left.header.stamp=rosTime
    camera_raw_right.header.stamp=rosTime
    camera_info_left.header.stamp=rosTime
    camera_info_right.header.stamp=rosTime

    camera_raw_left.header.frame_id=camera_info_left.header.frame_id
    camera_raw_right.header.frame_id=camera_info_right.header.frame_id

    cameraraw_left_pub.publish(camera_raw_left)
    cameraraw_right_pub.publish(camera_raw_right)
    camerainfo_left_pub.publish(camera_info_left)
    camerainfo_right_pub.publish(camera_info_right)

def synchronizer(source_namespace,target_namespace):
    global camerainfo_left_pub,camerainfo_right_pub
    global cameraraw_left_pub,cameraraw_right_pub
    rospy.init_node('camera_sync',anonymous=True)
    print source_namespace,"\t",target_namespace

    # unsynchronized topics
    rospy.Subscriber(source_namespace+'/left/image_raw',Image,camRaw_left)
    rospy.Subscriber(source_namespace+'/right/image_raw',Image,camRaw_right)
    rospy.Subscriber(source_namespace+'/left/camera_info',CameraInfo,camInfo_left)
    rospy.Subscriber(source_namespace+'/right/camera_info',CameraInfo,camInfo_right)

    # synchronized topics objects
    camerainfo_left_pub=rospy.Publisher(target_namespace+'/left/camera_info',CameraInfo,queue_size=10)
    camerainfo_right_pub=rospy.Publisher(target_namespace+'/right/camera_info',CameraInfo,queue_size=10)
    cameraraw_left_pub=rospy.Publisher(target_namespace+'/left/image_raw',Image,queue_size=10)
    cameraraw_right_pub=rospy.Publisher(target_namespace+'/right/image_raw',Image,queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Synchronize received Image frames and publish')
    parser.add_argument('--sourceNamespace',required=True,help='source namespace')
    parser.add_argument('--targetNamespace',required=True,help='target namespace')
    args = vars(parser.parse_args())
    synchronizer(source_namespace=args['sourceNamespace'],target_namespace=args['targetNamespace'])

