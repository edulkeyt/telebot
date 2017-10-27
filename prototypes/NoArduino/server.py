from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
import Adafruit_PCA9685
import RPi.GPIO as gpio

SG90_MAX_ANGLE = 180;

SG90_MIN_PULSE = 130
SG90_PULSE_DELTA = 470

SERVO_COMMAND_PARAMETER_NAME = "servos=";
WHEELS_COMMAND_PARAMETER_NAME = "wheels=";
GET_SERVO_POSITIONS_COMMAND = "getPositions";

SAVE_SERVO_SETTINGS_PARAMETER_NAME = "saveServoSettings/data=";
SERVO_SETTING_PATH = "settings/servo.txt"
SERVO_ARGUMENTS_SEPARATOR = 'a';

WHEELS_ARGUMENTS_SEPARATOR = ":";

SERVER_ADDRESS = ("", 8000)

PCA9685_FREQUENCY = 60

GPIO_EN_A_PIN = 13
GPIO_IN_1_PIN = 19
GPIO_IN_2_PIN = 16
GPIO_IN_3_PIN = 26
GPIO_IN_4_PIN = 20
GPIO_EN_B_PIN = 21

GPIO_PWM_FREQUENCY = 60;

GPIO_PWM_DEGREE = 100;
GPIO_PWM_CLIENT_DEGREE = 255;

class MyHandler(CGIHTTPRequestHandler):

    def setHeaders(self):
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers();

    def do_HEAD(self):
        self.setHeaders();
    
    def do_GET(self):

        def setServosPositionsFromDegreesStrings(strings):
            for i, substring in enumerate(strings):
                angle = int(substring);
                pulse = int(SG90_MIN_PULSE + angle * SG90_PULSE_DELTA / SG90_MAX_ANGLE);
                pca9685.set_pwm(i, 0, pulse);

        def setWheelsStateFromStrings(strings):
            leftWheelState = int(int(strings[0])/4);
            rightWheelState = int(int(strings[0])%4);
            #print(str(leftWheelState) + ' ' + str(rightWheelState))

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

            #leftWheelCycle = int(int(strings[1]) * GPIO_PWM_DEGREE / GPIO_PWM_CLIENT_DEGREE)
            #rightWheelCycle = int(int(strings[2]) * GPIO_PWM_DEGREE / GPIO_PWM_CLIENT_DEGREE)
            #leftWheelPWM.ChangeDutyCycle(leftWheelCycle)
            #rightWheelPWM.ChangeDutyCycle(rightWheelCycle)            

        command = self.path[1:];        

        if command.startswith(SERVO_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            anglesStrings = command[len(SERVO_COMMAND_PARAMETER_NAME):].split(SERVO_ARGUMENTS_SEPARATOR);
            setServosPositionsFromDegreesStrings(anglesStrings);
            return;

        if command.startswith(WHEELS_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            commandStrings = command[len(WHEELS_COMMAND_PARAMETER_NAME):].split(WHEELS_ARGUMENTS_SEPARATOR);
            setWheelsStateFromStrings(commandStrings);
            return;

        if command.startswith(SAVE_SERVO_SETTINGS_PARAMETER_NAME):
            self.setHeaders();
            servoSettingsFile = open(SERVO_SETTING_PATH, 'w');
            servoSettingsFile.write(urllib.parse.unquote(command[len(SAVE_SERVO_SETTINGS_PARAMETER_NAME):]));
            servoSettingsFile.close();
            return;


        if command == GET_SERVO_POSITIONS_COMMAND:
            self.setHeaders();
            servosAngles = bytes([90, 90, 90, 90, 90, 90]);

            servoSettingsFile = open(SERVO_SETTING_PATH, 'r');
            settingsJson = servoSettingsFile.read();
            servoSettingsFile.close();

            self.wfile.write(self.buildServosSettings(settingsJson, servosAngles).encode('ascii'));
            return;
        
        super().do_GET();
        
        return;

    def buildServosSettings(self, settingsJson, servosAngles):
        settingSubstr = settingsJson.split('"angle":');
        if len(settingSubstr) >= 0:
            result = settingSubstr[0];
        for i in range(len(settingSubstr)-1):
            result += self.buildServoSetting(settingSubstr[i+1],servosAngles[i]);
        return result

    def buildServoSetting(self, settingSubstr, servoAngle):
        return '"angle":' + str(servoAngle) + settingSubstr[settingSubstr.find(','):]

pca9685 = Adafruit_PCA9685.PCA9685()
pca9685.set_pwm_freq(PCA9685_FREQUENCY)

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_EN_A_PIN, gpio.OUT)
gpio.setup(GPIO_IN_1_PIN, gpio.OUT)
gpio.setup(GPIO_IN_2_PIN, gpio.OUT)
gpio.setup(GPIO_IN_3_PIN, gpio.OUT)
gpio.setup(GPIO_IN_4_PIN, gpio.OUT)
gpio.setup(GPIO_EN_B_PIN, gpio.OUT)

leftWheelPWM = gpio.PWM(GPIO_EN_A_PIN, GPIO_PWM_FREQUENCY)
rightWheelPWM = gpio.PWM(GPIO_EN_B_PIN, GPIO_PWM_FREQUENCY)

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()

leftWheelPWM.stop()
rightWheelPWM.stop()

gpio.cleanup()
