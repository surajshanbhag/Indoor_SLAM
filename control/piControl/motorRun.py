from __future__ import division
import motorDriver.pwm as pwm_mod
import time
import socket_class as socket
import sys
import numpy as np

speed=0.5
RMotorCh = None
LMotorCh = None

servo_min = None
servo_nut = None
servo_max = None



def pwm_setup():
    global RMotorCh,LMotorCh
    global servo_min,servo_nut,servo_max

    pwm = pwm_mod.PCA9685()
    #set frequency to 50 Hz
    pwm.set_pwm_freq(50)
    #p = 1/freq = 1/50 = 20ms
    #"tick" = 20ms / 4096 = 4.883us
    tick = 4.883

    #mim = 553us 553/4.886 = 113
    servo_min = 553/tick
    #max = 2520us 2520/4.886 = 516
    servo_max = 2520/tick
    #neuteral = 1536us 1536/4.886 = 314.47
    servo_nut = 1536.5/tick

    RMotorCh = 0
    LMotorCh = 2

    return pwm

def run_motors_call(pwm,R_vel, L_vel):
    global RMotorCh,LMotorCh
    global servo_min,servo_nut,servo_max,speed


    if(RMotorCh is None or LMotorCh is  None):
        print("Motors not setup")
        return
    #print(R_vel)
    #print(L_vel)
    R = int((((servo_max-servo_min)/2)*R_vel*speed+servo_nut))
    L = int((((servo_max-servo_min)/2)*-L_vel*speed+servo_nut))

    print(R,L)
    pwm.set_pwm(RMotorCh,0,R)
    pwm.set_pwm(LMotorCh,0,L)

def test(pwm):
    pwm.set_pwm(0,0,307)
    pwm.set_pwm(2,0,307)


if __name__ == "__main__":
    pwm = pwm_setup()
    print("Starting Test")
    s = socket.initSocket()
    while True:
        try:
            if len(sys.argv) == 3:
                socket.connect(s,sys.argv[1],int(sys.argv[2]))
            else:
                socket.connect(s,"10.42.0.1",50676)
            break
        except:
            pass
    while True:
        rec = s.recv(4096)
        if(rec == "stop"):
            break
        s.send("OK")
        R,L = rec.split(",")
        R = np.float32(R)
        L = np.float32(L)
        print(R,L)
        run_motors_call(pwm,R,L)
    print("Done")
