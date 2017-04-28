from __future__ import division
import time
from threading import Timer
import RPi.GPIO as GPIO
global encoder_values
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pin definition
CLK = None
DOUTR = None
CSR = None
DOUTL = None
CSL = None
encoder_values=[[0]*512,[0]*512]

waitTime = .00005
def getEncoder(funcR, funcL, threshold = [270,300,270,290]):
    """Reads encoder values. Runs call back function on color change thresholds can be over written
    Inputs:
    funcR - function to run on right transition 
    funcL - function to run on left transitions
    threshold - format [Right low, Right high, Left low, Left high]
    """
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

def encoderSetup(CLKin = 13, DOUTRin = 20, CSRin = 19, DOUTLin = 21, CSLin = 16):
    """configures encoder GPIPO pins"""
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
    """read ADC to get encoder value"""
    global encoder_values
    global CLK,DOUTR,DOUTL,CSR,CSL
    ADCdataR=0
    ADCdataL=0
    #raise chip select to start transaction 
    GPIO.output(CSL, True)
    GPIO.output(CSR, True)
    time.sleep(waitTime)
    time.sleep(waitTime)
    GPIO.output(CSL, False)
    GPIO.output(CSR, False)
    
    #read in data from ADC
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

    #store values for debugging purposes 
    encoder_values[0][ADCdataR]+=1
    encoder_values[1][ADCdataL]+=1
    #print("Output R is",ADCdataR,"    Output L is",ADCdataL)

    return((ADCdataR, ADCdataL))


if __name__ == "__main__":
    encoderSetup()
    count = 2000
    while count:
        readEncoder()
        count-=1
        #time.sleep(0.50)
        
    #print 2000 measure ADC value to get encode characteristics     
    print 'right'
    for index,val in enumerate(encoder_values[0]):
        if val:
            print index,'\t',val

    print 'left'
    for index,val in enumerate(encoder_values[1]):
        if val:
            print index,'\t',val
    GPIO.cleanup()#to release any resources that script is using
