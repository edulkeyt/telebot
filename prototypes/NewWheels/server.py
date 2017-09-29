from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import serial
import urllib

SERIAL_PORT = '/dev/ttyUSB0';
SERIAL_BAUD_RATE = 9600;
SERIAL_TIMEOUT = 20;

SERVO_COMMAND_PARAMETER_NAME = "servos=";
WHEELS_COMMAND_PARAMETER_NAME = "wheels=";
WHEELS_COMMAND_CODE = 200;
GET_SERVO_POSITIONS_COMMAND = "getPositions";
GET_SERVO_POSITIONS_COMMAND_CODE = 255;

SAVE_SERVO_SETTINGS_PARAMETER_NAME = "saveServoSettings/data=";
SERVO_SETTING_PATH = "settings/servo.txt"

SERVER_ADDRESS = ("", 8000)

class MyHandler(CGIHTTPRequestHandler):

    def setHeaders(self):
        self.send_response(200);
        self.send_header('Content-type', 'text/html');
        self.end_headers();

    def do_HEAD(self):
        self.setHeaders();
    
    def do_GET(self):

        def bytesToStringOfNumbers(byteArray):
            result = "[";
            for i in byteArray:
                result += str(int(i)) + ",";           
            return result[0:-1] + "]";

        def stringArrayToIntBytes(strings):
            result = [];
            for substring in strings:
                #result.append(bytes([int(substring)]));
                result.append(int(substring));
            return result;

        command = self.path[1:];        

        if command.startswith(SERVO_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            anglesStrings = command[len(SERVO_COMMAND_PARAMETER_NAME):].split('a');
            serialBytes = stringArrayToIntBytes(anglesStrings);
            ser.write(bytes(serialBytes));            
            return;

        if command.startswith(WHEELS_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            commandString = command[len(WHEELS_COMMAND_PARAMETER_NAME):];
            commandInt = [];
            commandInt.append(WHEELS_COMMAND_CODE);
            commandInt.append(int(commandString));
            ser.write(bytes(commandInt));
            return;

        if command.startswith(SAVE_SERVO_SETTINGS_PARAMETER_NAME):
            self.setHeaders();
            servoSettingsFile = open(SERVO_SETTING_PATH, 'w');
            servoSettingsFile.write(urllib.parse.unquote(command[len(SAVE_SERVO_SETTINGS_PARAMETER_NAME):]));
            servoSettingsFile.close();
            return;


        if command == GET_SERVO_POSITIONS_COMMAND:
            self.setHeaders();
            ser.write(bytes([GET_SERVO_POSITIONS_COMMAND_CODE]));
            time.sleep(SERIAL_TIMEOUT * 4 / 1000);
            serialBytesAvaible = ser.inWaiting();
            servosAngles = ser.readline(serialBytesAvaible);
            #print(bytesToStringOfNumbers(servosAngles));

            servoSettingsFile = open(SERVO_SETTING_PATH, 'r');
            settingsJson = servoSettingsFile.read();
            #print(settingsJson);
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

#ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE)

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()
