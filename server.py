from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import urllib
from wheels import WheelsController
from servos import ServosController

SERVO_COMMAND_PARAMETER_NAME = "servos=";
WHEELS_COMMAND_PARAMETER_NAME = "wheels=";

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
            servos.setServosPositionsFromDegreesStrings(anglesStrings);
            return;

        if command.startswith(WHEELS_COMMAND_PARAMETER_NAME):
            self.setHeaders();
            commandStrings = command[len(WHEELS_COMMAND_PARAMETER_NAME):].split(WHEELS_ARGUMENTS_SEPARATOR);
            wheels.setWheelsStateFromStrings(commandStrings);
            return;

        super().do_GET();        
        return;

servos = ServosController();

wheels = WheelsController();

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()

wheels.dispose();
