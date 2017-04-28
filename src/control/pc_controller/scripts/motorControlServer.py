#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import server

global mode, pub, prevbutton
global R_vel, L_vel
global reply
global c
py_clip = lambda x, mn, mx: mn if x < mn else mx if x > mx else x
py_dead_zone = lambda x, mn, mx: x if x < mn else x if x > mx else 0

py_joytrim = lambda x: py_clip(py_dead_zone(x,-.05,.05),-1,1)

auto=1
manual=0
offset=[0.4,.17]#left,right
speed=0.5

def joy_call(data):
    """joystick callback function must be configured for your joystick
        currently configured for xbox360 controller"""
    global prevbutton, mode
    global R_vel, L_vel
    global reply
    global c

    #toggle between manual and auto control using A button
    #auto control not implemented 
    if data.buttons[0]==1 and prevbutton==0:
        if mode == 1:
            mode=0
        else:
            mode=1

    prevbutton=data.buttons[0]

    if data.axes[6] == 1:
        #Turn left on left D-pad press
        R_vel=speed*offset[1]
        L_vel=0
    elif data.axes[6] == -1:
        #Turn right on right D-pad press
        R_vel=0
        L_vel=speed*offset[0]
    elif data.axes[4] > 0.9:
        #Go forward when Right Stick is forward
        R_vel=speed*offset[1]
        L_vel=speed*offset[0]
    else:
        R_vel=0
        L_vel=0



def main():
    global R_vel, L_vel
    global mode, pub, prevbutton
    global reply
    global c
    R_vel = 0
    L_vel = 0
    mode = manual
    
    #start socket
    s = server.initialize_Socket()
    
    #wait for connection
    c, addr = s.accept()
    print("Got connection from", addr)
    reply = ""
    
    #init ROS node
    rospy.init_node("motorValues", anonymous=True)
    #subscribe to joystick
    rospy.Subscriber("joy", Joy, joy_call)

    rate=rospy.Rate(100)

    #publish motor control values on port 4096
    while not rospy.is_shutdown():
        if mode == manual:
            reply = ""
            print "right :"+ str(R_vel) + "\t left :" +str(L_vel)
            c.send(str(R_vel)+","+str(L_vel));
            reply = c.recv(4096)

            if not reply:
                print("Broken Pipe")

        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
