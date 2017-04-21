from __future__ import division
import time
from threading import Timer
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin definition
CLK = None
DOUTR = None
CSR = None
DOUTL = None
CSL = None

waitTime = .00005
def getEncoder(funcR, funcL, threshold = [285,300,285,300]):
    R_flag = [False,False]
    L_flag = [False,False]
    R_last, L_last = (0,0)
    while True:
        R,L = readEncoder()
        #print R,L
        if(not R_flag and R<threshold[0] and R_last<threshold[0]):
            R_flag = True
            funcR()
        elif(R_flag and R>threshold[1] and R_last>threshold[1]):
            R_flag = False
            funcR()
        if(not L_flag and L<threshold[2] and L_last<threshold[2]):
            L_flag = True
            funcL()
        elif(L_flag and L>threshold[3] and L_last<threshold[3]):
            L_flag = False
            funcL()
        L_last = L
        R_last = R

def getWheelSpeed(numSamples = 8, diameter = 8.5, threshold = [315,290], n = 20):
#diameter given in cm, threshold may depend on lightlevels, n is the number of devisions on the wheel
    R_count = 0
    L_count= 0
    R_high = []
    L_high = []
    R_low = []
    L_low = []
    R_flag = False
    L_flag = False
    count = 0
    while True:
        R,L = readEncoder()
        if(not R_flag and R<threshold[0]):
            R_low.append(time.time())
            R_flag = True
        elif(R_flag and R>threshold[0]):
            R_high.append(time.time())
            R_flag = False
            R_count+=1
        if(not L_flag and L<threshold[1]):
            L_low.append(time.time())
            L_flag = True
        elif(L_flag and L>threshold[1]):
            L_high.append(time.time())
            L_flag = False
            L_count+=1
        if(L_count > numSamples and R_count > numSamples):
            break
    time_diff = []
    for low, high in zip(R_low,R_high):
        time_diff.append(high-low)

    R_avg = sum(time_diff[1:])/len(time_diff[1:])
    print "R-time_diff ", time_diff
    time_diff = []
    for low, high in zip(L_low,L_high):
         time_diff.append(high-low)

    L_avg = sum(time_diff[1:])/len(time_diff[1:])
    print "L-time_diff ", time_diff
    #speed = D/T, D = C of wheel
    #C = d*pi, speed = d*pi/(t*n)

    R_speed = (diameter*3.14159)/(R_avg*n*100)
    L_speed = (diameter*3.14159)/(L_avg*n*100)

    return(R_speed,L_speed)

def encoderSetup(CLKin = 13, DOUTRin = 20, CSRin = 19, DOUTLin = 21, CSLin = 16):
    global CLK,DOUTR,DOUTL,CSR,CSL
    CLK = CLKin
    DOUTR = DOUTRin
    DOUTL = DOUTLin
    CSR = CSRin
    CSL = CSLin

    GPIO.setup(CLK,GPIO.OUT)
    GPIO.setup(DOUTR,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CSR,GPIO.OUT)
    GPIO.setup(DOUTL,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(CSL,GPIO.OUT)


def readEncoder():
    global CLK,DOUTR,DOUTL,CSR,CSL
    ADCdataR=0
    ADCdataL=0
    GPIO.output(CSL, True)
    GPIO.output(CSR, True)
    time.sleep(waitTime)
    time.sleep(waitTime)
    GPIO.output(CSL, False)
    GPIO.output(CSR, False)
    for x in range (0,1):
      if (GPIO.input(CLK)== True):
          GPIO.output(CLK, False)
      else:
        GPIO.output(CLK, True)
        time.sleep(waitTime)
        time.sleep(waitTime)
    for i in range (0,16):
      if GPIO.input(CLK)== True:
        time.sleep(waitTime)
        time.sleep(waitTime)
        if GPIO.input(DOUTR)== True:
           ADCdataR+=1
        ADCdataR<<=1
        if GPIO.input(DOUTL)== True:
           ADCdataL+=1
        ADCdataL<<=1
        GPIO.output(CLK, False)
        time.sleep(waitTime)
        time.sleep(waitTime)
      else:
        GPIO.output(CLK, True)
        time.sleep(waitTime)
        time.sleep(waitTime)

    #print("Output R is",ADCdataR)
    #print("Output L is",ADCdataL)

    return((ADCdataR, ADCdataL))
if __name__ == "__main__":
    encoderSetup()
    while True:
        readEncoder()
        time.sleep(0.50)
    GPIO.cleanup()#to release any resources that script is using
