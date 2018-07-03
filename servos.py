import Adafruit_PCA9685

SG90_MAX_ANGLE = 180;
SG90_MIN_PULSE = 130
SG90_PULSE_DELTA = 470

PCA9685_FREQUENCY = 60

class ServosController:

	pca9685 = Adafruit_PCA9685.PCA9685()
	pca9685.set_pwm_freq(PCA9685_FREQUENCY)

	def setServosPositionsFromDegreesStrings(self, strings):
	    for i, substring in enumerate(strings):
	        angle = int(substring);
	        pulse = int(SG90_MIN_PULSE + angle * SG90_PULSE_DELTA / SG90_MAX_ANGLE);
	        self.pca9685.set_pwm(i, 0, pulse);
