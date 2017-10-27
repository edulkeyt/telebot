import time
import Adafruit_PCA9685

SG90_MIN_PULSE = 130
SG90_MAX_PULSE = 600

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

pwm.set_pwm(0, 0, SG90_MIN_PULSE)
time.sleep(3)
pwm.set_pwm(0, 0, SG90_MAX_PULSE)
time.sleep(3)
