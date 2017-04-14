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
import multiprocessing
import threading

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

def receiver(client_ip,client_port,image_buffer,lock,image_update):

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.bind((CLIENT_IP, CLIENT_PORT))
    sock.bind(('', client_port))
    pic=''
    temp=-1
# ROS stuf
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
                cv2.imshow('frame',res)
                print "Acquire Lock  " + client_ip
                try:
                    #lock.acquire()
                    #print "Lock acquired " + client_ip
                    image_buffer.append(img)
                    #lock.release()
                    image_update=True
                    #print "Lock released " + client_ip
                except:
                    pass
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break;
        except:
            pass
        pic=''

def publishMessages(left_image_buffer,right_image_buffer,left_image_updated,right_image_updated,image_buffer,process_lock,calibration_file):
    image_publisher=[]
    cameraInfo_publisher=[]
    camera_info=[]
    left_image=[]
    right_image=[]
    image_publisher.append(rospy.Publisher("/camera/left/image_raw",Image,queue_size=10))
    image_publisher.append(rospy.Publisher("/camera/right/image_raw",Image,queue_size=10))
    cameraInfo_publisher.append(rospy.Publisher("/camera/left/camera_info",CameraInfo,queue_size=10))
    cameraInfo_publisher.append(rospy.Publisher("/camera/right/camera_info",CameraInfo,queue_size=10))

    camera_info.append(CameraInfo())
    camera_info.append(CameraInfo())
    parse_yaml(calibration_file[0],camera_info[0])
    parse_yaml(calibration_file[1],camera_info[1])

    rospy.init_node('camera_streamer',anonymous=True)
    bridge=CvBridge()
    right_image_received=False
    left_image_received=False

    while True:
        if not left_image_buffer:    # image buffer is empty
            print "no image in left image buffer"
            pass
        else:
            try:
                process_lock[0].acquire
                left_image=left_image_buffer.pop(0)
                left_image_received=True
                left_image_updated=False
                process_lock[0].release()
            except:
                print "Waiting for Left image process lock ..."
                pass

        if not right_image_buffer:    # image buffer is empty
            print "no image in right image buffer"
            pass
        else:
            try:
                process_lock[1].acquire
                right_image=right_image_buffer.pop(0)
                right_image_received=True
                right_image_updated=False
                process_lock[1].release()
            except:
                print "Waiting for Right image process lock ..."
                pass

        if right_image_received == True and left_image_received == True:
                print "ROS Published"
                image_publisher[0].publish(bridge.cv2_to_imgmsg(left_image, "bgr8"))
                image_publisher[1].publish(bridge.cv2_to_imgmsg(right_image, "bgr8"))
                camera_info[0].header.stamp=rospy.Time.from_sec(time.time())
                camera_info[1].header.stamp=rospy.Time.from_sec(time.time())
                cameraInfo_publisher[0].publish(camera_info)
                cameraInfo_publisher[1].publish(camera_info)
                right_image_received=False
                left_image_received=False



if __name__ == '__main__':
    left_image_buffer=[]
    right_image_buffer=[]

    filename=[sys.argv[1],sys.argv[2]]

    process_lock=[]
    process_lock.append(threading.Lock())
    process_lock.append(threading.Lock())

    right_image_updated=False
    left_image_updated=False

    left_process=threading.Thread(target=receiver,args=('10.42.0.1',50677,left_image_buffer,process_lock[0],right_image_updated))
    right_process=threading.Thread(target=receiver,args=('10.42.0.1',50678,right_image_buffer,process_lock[1],left_image_updated))

    #left_process=multiprocessing.Process(target=receiver,args=('10.42.0.1',50677,left_image_buffer,process_lock[0],right_image_updated))
    #right_process=multiprocessing.Process(target=receiver,args=('10.42.0.1',50678,right_image_buffer,process_lock[1],left_image_updated))


    publish_message_process=multiprocessing.Process(target=publishMessages,args=(left_image_buffer,right_image_buffer,left_image_updated,right_image_updated,process_lock,filename))

    left_process.start()
    right_process.start()
    time.sleep(1)
    publish_message_process.start()

    while True:
        pass


