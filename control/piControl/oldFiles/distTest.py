import encoder
import motorTest as pwm_mod
import time

rightC, leftC = (0,0)

def right():
    global rightC
    rightC += 1
    print"Right: ",rightC

def left():
    global leftC
    leftC += 1
    print "Left: ",leftC

if __name__ == "__main__":
    #pwm = pwm_mod.pwm_setup()
    #start = time.time()
    #stop = time.time()
    encoder.encoderSetup()
    #pwm_mod.run_motors_call(pwm,1,1)
    encoder.getEncoder(right,left)
    #while stop-start < 10:   
    #print "Speed: ", encoder.getWheelSpeed()
    #print "Speed: ", encoder.getWheelSpeed()
    #print "Speed: ", encoder.getWheelSpeed()
    #stop = time.time()
    #pwm_mod.run_motors_call(pwm, 0,0)
    #print (stop-start), " Seconds"
