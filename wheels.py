import RPi.GPIO as gpio

GPIO_EN_A_PIN = 13
GPIO_IN_1_PIN = 19
GPIO_IN_2_PIN = 16
GPIO_IN_3_PIN = 26
GPIO_IN_4_PIN = 20
GPIO_EN_B_PIN = 21

GPIO_PWM_FREQUENCY = 60;

GPIO_PWM_DEGREE = 100;
GPIO_PWM_CLIENT_DEGREE = 255;

class WheelsController:

        gpio.cleanup()
        gpio.setmode(gpio.BCM)

        gpio.setup(GPIO_EN_A_PIN, gpio.OUT)
        gpio.setup(GPIO_IN_1_PIN, gpio.OUT)
        gpio.setup(GPIO_IN_2_PIN, gpio.OUT)
        gpio.setup(GPIO_IN_3_PIN, gpio.OUT)
        gpio.setup(GPIO_IN_4_PIN, gpio.OUT)
        gpio.setup(GPIO_EN_B_PIN, gpio.OUT)

        leftWheelPWM = gpio.PWM(GPIO_EN_A_PIN, GPIO_PWM_FREQUENCY)
        rightWheelPWM = gpio.PWM(GPIO_EN_B_PIN, GPIO_PWM_FREQUENCY)
        leftWheelPWM.start(0);
        rightWheelPWM.start(0);

        def dispose(self):
                leftWheelPWM.stop()
                rightWheelPWM.stop()
                gpio.cleanup()
		
        def setWheelsStateFromStrings(self, strings):
                leftWheelState = int(int(strings[0])/4);
                rightWheelState = int(int(strings[0])%4);
		
                if leftWheelState == 0:
                        gpio.output(GPIO_IN_1_PIN, False);
                        gpio.output(GPIO_IN_2_PIN, False);
                elif leftWheelState == 1:
                        gpio.output(GPIO_IN_1_PIN, True);
                elif leftWheelState == 2:
                        gpio.output(GPIO_IN_2_PIN, True);

                if rightWheelState == 0:
                        gpio.output(GPIO_IN_3_PIN, False);
                        gpio.output(GPIO_IN_4_PIN, False);
                elif rightWheelState == 1:
                        gpio.output(GPIO_IN_4_PIN, True);
                elif rightWheelState == 2:
                        gpio.output(GPIO_IN_3_PIN, True);

                leftWheelCycle = int(int(strings[1]) * GPIO_PWM_DEGREE / GPIO_PWM_CLIENT_DEGREE)
                rightWheelCycle = int(int(strings[2]) * GPIO_PWM_DEGREE / GPIO_PWM_CLIENT_DEGREE)
                self.leftWheelPWM.ChangeDutyCycle(leftWheelCycle)
                self.rightWheelPWM.ChangeDutyCycle(rightWheelCycle)
