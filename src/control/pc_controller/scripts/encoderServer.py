#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist, Pose, Vector3,Quaternion, Point, TransformStamped
import geometry_msgs.msg
from nav_msgs.msg import Odometry
import tf
import math
import time
import socket

global prev_distance,distance,Odometry_pub,robot_Heading,robot_pos
def initiliaze_Socket():
    s=socket.socket()
    print "Socket created"

    port =50679

    s.bind(('',port))
    print "socket bound to %s" %(port)

    s.listen(5)
    print 'socket is listening'
    return s

def publish_odom(data):
    global prev_distance,distance,Odometry_pub,robot_Heading,robot_pos
    encoder_Data=data.split(',')

    if len(encoder_Data) != 2:
        return 0
    #each increment is 0.01319mm of travel
    distance=[int(side)*0.0065188 for side in encoder_Data]
    #print "distance " , distance
    #print "prev_distance " ,prev_distance

    displacement=[cur-prev for cur,prev in zip(distance,prev_distance)]
    displacement_robot=(sum(displacement))/2
    rotation_robot=(displacement[0]-displacement[1])/0.155
    #rotation_robot/=2

    robot_Heading+=rotation_robot

    if rotation_robot == 0:
        radius_robot=displacement_robot
    else:
        radius_robot=displacement_robot/rotation_robot
        if robot_Heading > 2*math.pi:
            robot_Heading -= 2*math.pi
        elif robot_Heading < 0:
            robot_Heading += 2 * math.pi
    #print "robot_Heading", robot_Heading
    #print "rotation_robot ", rotation_robot
    #print "displacement_robot" ,displacement_robot
    robot_pos[0]=robot_pos[0] + displacement_robot*math.cos(robot_Heading)
    robot_pos[1]=robot_pos[1] + displacement_robot*math.sin(robot_Heading)

    current_time=rospy.Time.now()

    odom_quat=tf.transformations.quaternion_from_euler(0.0,0.0,robot_Heading)
    tf_broadcaster=tf.TransformBroadcaster()

    tf_broadcaster.sendTransform((robot_pos[0],robot_pos[1],0),odom_quat,current_time
            ,"base_link","odom")

    odom=Odometry()
    odom.header.stamp=current_time
    odom.header.frame_id="odom"
    odom.pose.pose=Pose(Point(robot_pos[0],robot_pos[1],0),Quaternion(*odom_quat))
    odom.child_frame_id="base_link"
    #print robot_pos
    try:
        Odometry_pub.publish(odom)
    except:
        print "publish error"

    prev_distance=distance




if __name__ == '__main__':
    global prev_distance,distance,Odometry_pub,robot_Heading,robot_pos
    distance=[0,0]
    prev_distance=[0,0]
    robot_Heading=0
    robot_pos=[0,0]
    rospy.init_node('robot_encoder')
    Odometry_pub=rospy.Publisher('robot_encoder/odom',Odometry,queue_size=10)
    s=initiliaze_Socket()
    c, addr=s.accept()
    #print 'got connection from ' , addr
    while True:
        received=c.recv(100)
        c.send('OK')
        #print received
        publish_odom(received)
    #print 'Test Done'
