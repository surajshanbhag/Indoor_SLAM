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
    #return cam_info

def receiver(filename,port=50678):
    CLIENT_IP='10.42.0.1'
    CLIENT_PORT = port
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind((CLIENT_IP, CLIENT_PORT))
    sock.bind(('', CLIENT_PORT))
    pic=''
    temp=-1
# ROS stuf
    image_publisher=rospy.Publisher("/camera/right/image_raw",Image,queue_size=10)
    cameraInfo_publisher=rospy.Publisher("/camera/right/camera_info",CameraInfo,queue_size=10)
    rospy.init_node('right_camera_streamer',anonymous=True)
    bridge=CvBridge()
    camera_info=CameraInfo()
    parse_yaml(filename,camera_info)
    camera_info.height=600
    camera_info.width=800
    while True:
        temp=-1
        flag=0
        while True:
            data, addr = sock.recvfrom(20480)
            seq=struct.unpack('I',data[0:4])[0]
            try:
                if struct.unpack('I',data[4:8])[0]==9999:
                    break
            except:
                pass
            if seq-1>temp:
                print 'error'
                flag=1
            temp=seq
            pic=pic+data[4:]
        if seq != temp+1:
            flag=1
        try:
            if flag==0:
                img=cv2.imdecode(np.asarray(bytearray(pic),dtype=np.uint8), 1)
                res = cv2.resize(img,None,fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
        except:
            flag=1
        try:
            if flag==0:
                #cv2.imshow('frame',res)
                camera_info.header.stamp=rospy.Time.from_sec(time.time())
                cameraInfo_publisher.publish(camera_info)
                image_publisher.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break;
        except:
            pass
        pic=''

if __name__ == '__main__':
    if (len(sys.argv[1]) == 1):
        receiver(filename='right.yaml',port=50678)
    else:
        receiver(filename=sys.argv[1],port=50678)
