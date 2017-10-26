import time
import RPi.GPIO as io

io.setmode(io.BCM)

enAPin = 13
in1Pin = 19
in2Pin = 16
in3Pin = 26
in4Pin = 20
enBPin = 21

pwmFrequency = 50

io.setup(enAPin, io.OUT)
io.setup(in1Pin, io.OUT)
io.setup(in2Pin, io.OUT)
io.setup(in3Pin, io.OUT)
io.setup(in4Pin, io.OUT)
io.setup(enBPin, io.OUT)

leftWheelPWM = io.PWM(enAPin, pwmFrequency)
rightWheelPWM = io.PWM(enBPin, pwmFrequency)

leftWheelPWM.start(0)
rightWheelPWM.start(0)

io.output(in1Pin, True)
io.output(in4Pin, True)

try:
    while 1:
        for dc in range(0, 101, 5):
            leftWheelPWM.ChangeDutyCycle(dc)
            rightWheelPWM.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            leftWheelPWM.ChangeDutyCycle(dc)
            rightWheelPWM.ChangeDutyCycle(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass

leftWheelPWM.stop()
rightWheelPWM.stop()

io.cleanup()

