import motorRun as pwm_mod
import time
pwm = pwm_mod.pwm_setup()

#simple script turn motors on waits than turn motors off 
#used to test PWM settings and balance motor speeds

if __name__ == "__main__":
      pwm = pwm_mod.pwm_setup()
      pwm_mod.run_motors_call(pwm,.2,.2)
      print "Starting"
      time.sleep(15)
      print "Stoping"
      pwm_mod.run_motors_call(pwm, 0,0)
