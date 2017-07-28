from http.server import HTTPServer, CGIHTTPRequestHandler
import time
import serial

SERIAL_PORT = 'COM3';
SERIAL_BAUD_RATE = 9600;
SERIAL_TIMEOUT = 10;

LEFT_COMMAND = "left";
RIGHT_COMMAND = "right";
STOP_COMMAND = "stop";

COMANDS_LIST = []
RESPONSE_COMANDS_LIST = [LEFT_COMMAND, RIGHT_COMMAND, STOP_COMMAND]

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

        if any(command == c for c in COMANDS_LIST):
            self.setHeaders();
            print(command);
            ser.write(command.encode('ascii'));
            return;

        if any(command == c for c in RESPONSE_COMANDS_LIST):
            self.setHeaders();
            print(command);
            ser.write(command.encode('ascii'));
            time.sleep(SERIAL_TIMEOUT * 3 / 1000);
            serialBytesAvaible = ser.inWaiting();
            serialOut = ser.readline(serialBytesAvaible);
            self.wfile.write(serialOut);
            print(serialOut);
            return;
        
        super().do_GET();
        
        return;


ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD_RATE)

httpd = HTTPServer(SERVER_ADDRESS, MyHandler)
print("Server started")
httpd.serve_forever()
