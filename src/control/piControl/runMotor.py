import motorRun as pwm_mod
import time
pwm = pwm_mod.pwm_setup()
if __name__ == "__main__":
      pwm = pwm_mod.pwm_setup()
      #pwm_mod.run_motors_call(pwm,1,1)
      print "Starting"
      #time.sleep(3)
      #print "Stoping"
      pwm_mod.run_motors_call(pwm, 0,0)
