from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
from wheels.py import WheelsController
from servos.py import ServosController

SERVO_COMMAND_PARAMETER_NAME = "servos=";
WHEELS_COMMAND_PARAMETER_NAME = "wheels=";
GET_SERVO_POSITIONS_COMMAND = "getPositions";

SAVE_SERVO_SETTINGS_PARAMETER_NAME = "saveServoSettings/data=";
SERVO_SETTING_PATH = "settings/servo.txt"
SERVO_ARGUMENTS_SEPARATOR = 'a';

WHEELS_ARGUMENTS_SEPARATOR = ":";

SERVER_ADDRESS = ("", 8000)

class MyHandler(CGIHTTPRequestHandler):

    def setHeaders(self):
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers();

    def do_HEAD(self):
        self.setHeaders();
    
    def do_GET(self):

        command = self.path[1:];        

        if command.startswith(SERVO_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            anglesStrings = command[len(SERVO_COMMAND_PARAMETER_NAME):].split(SERVO_ARGUMENTS_SEPARATOR);
            setServosPositionsFromDegreesStrings(anglesStrings);
            return;

        if command.startswith(WHEELS_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            commandStrings = command[len(WHEELS_COMMAND_PARAMETER_NAME):].split(WHEELS_ARGUMENTS_SEPARATOR);
            wheels.setWheelsStateFromStrings(commandStrings);
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

servos = ServosController();
servos.init();

wheels = WheelsController();
wheels.init();

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()

wheels.dispose();
