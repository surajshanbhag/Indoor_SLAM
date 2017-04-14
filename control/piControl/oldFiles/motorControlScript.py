#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from xbox1control.msg import velocities
import motorDriver.pwm as pwm_mod

RMotorCh = None
LMotorCh = None

def pwm_setup():
    pwm = pwm_mod.PCA9685()
    #set frequency to 50 Hz
    pwm.set_pwm_freq(50)
    #p = 1/freq = 1/50 = 20ms
    #"tick" = 20ms / 4096 = 4.886us

    #mim = 900us 900/4.886 = 185
    servo_min = 185
    #max = 2100us 2100/4.886 = 430
    servo_max = 430
    #neuteral = 1500us 1500/4.886 = 307
    servo_nut = 307

    RMotorCh = 0
    LMotorCh = 2


def run_motors_call(vel):
    if(RMotorCh is None or LMotorCh is  None):
	print("Motors not setup")
        return
    #print(vel.R_vel)
    #print(vel.L_vel)
    R = ((servo_max-servo_min)/2)*vel.R_vel+servo_nut
    L = ((servo_max+servo_min)/2)*-vel.L_vel+servo_nut

    pwm.setPWM(RMotorCh,0,R)
    pwm.setPWM(LMotorCh,0,L)

def main():
    pwm_setup()
    rospy.init_node("motor_run",  anonymous=True)
    rospy.Subscriber("MotorControlValues", velocities, run_motors_call)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
