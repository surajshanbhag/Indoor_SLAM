import encoder
import motorTest as pwm_mod

if __name__ == "__main__":
    encoder.encoderSetup()
    min = [500,500]
    max = [0,0]
    count = 0
    pwm = pwm_mod.pwm_setup()
    pwm_mod.run_motors_call(pwm,1,1)
    while True:
       R,L = encoder.readEncoder()
       if R<min[0]:
           min[0]=R
       if R>max[0]:
           max[0]=R

       if L<min[1]:
           min[1]=L
       if L>max[1]:
           max[1]=L
       count+=1
       if(count >1000):
            break
    pwm_mod.run_motors_call(pwm, 0,0)
    print "min: ", min
    print "max: ", max

    
