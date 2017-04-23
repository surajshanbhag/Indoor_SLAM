#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
#from xbox1control.msg import velocities
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
offset=[2,.9]
speed=0.1

def joy_call(data):
    global prevbutton, mode
    global R_vel, L_vel
    global reply
    global c

    if data.buttons[0]==1 and prevbutton==0:
        if mode == 1:
            mode=0
        else:
            mode=1

    prevbutton=data.buttons[0]

    #R_vel = py_joytrim((data.axes[0]+data.axes[1]))
    #L_vel = py_joytrim((data.axes[0]-data.axes[1]))

    if data.axes[6] == 1:
        R_vel=speed*offset[1]
        L_vel=0
    elif data.axes[6] == -1:
        R_vel=0
        L_vel=speed*offset[0]
    elif data.axes[4] > 0.9:
        R_vel=speed*offset[1]
        L_vel=speed*offset[0]
    else:
        R_vel=0
        L_vel=0

    #R_vel = py_joytrim((data.axes[1]+data.axes[0]))
    #L_vel = py_joytrim((data.axes[1]-data.axes[0]))

    #print "reply :" + reply
    #reply = ""
    #while reply != "OK":
    #    print "right :"+ str(R_vel) + "\t left :" +str(L_vel)
    #    c.send(str(R_vel)+","+str(L_vel));
    #    reply = c.recv(4096)
    #
    #    if not reply:
    #        print("Broken Pipe")
    #        break

def main():
    global R_vel, L_vel
    global mode, pub, prevbutton
    global reply
    global c
    R_vel = 0
    L_vel = 0
    mode = auto
    s = server.initialize_Socket()
    c, addr = s.accept()
    print("Got connection from", addr)
    reply = ""

    rospy.init_node("motorValues", anonymous=True)
    rospy.Subscriber("joy", Joy, joy_call)

    #pub = rospy.Publisher('MotorControlValues', velocities, queue_size=10)

    rate=rospy.Rate(100)

    while not rospy.is_shutdown():
        if mode == manual:
            reply = ""
                #    pub.publish(R_vel,L_vel)
            #print("R_val: "+str(R_vel))
            #print("L_vel: "+str(L_vel))
            print "right :"+ str(R_vel) + "\t left :" +str(L_vel)
            c.send(str(R_vel)+","+str(L_vel));
            reply = c.recv(4096)

            if not reply:
                print("Broken Pipe")
            #    break

        else:
            pass
                #pub.publish()

        rate.sleep()
    #rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
