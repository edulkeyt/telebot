#include <Servo.h>

const short SERIAL_BAUD_RATE = 9600;
const short SERIAL_TIMEOUT = 10;

const short SERVO_PIN = 9;

const String LEFT_COMMAND = "left";
const String RIGHT_COMMAND = "right";
const String STOP_COMMAND = "stop";

const short MAX_ANGLE = 180;
const short MIN_ANGLE = 0;


const short SERVO_DELAY = 15;
const short SERVO_MAX_TIMES = 20;
const short SERVO_SPEED = 1;//can be modified. Other servo consts are optimal hardware settings

Servo controlledServo;
short servoPosition = (MAX_ANGLE + MIN_ANGLE) / 2;
bool servoDirectionRight = true;
short servoTimes = 0;

String serialIn;
bool sendPosition = false;

void setup() {
  
  Serial.begin(SERIAL_BAUD_RATE);
  Serial.setTimeout(SERIAL_TIMEOUT);
  
  controlledServo.attach(SERVO_PIN); 
}

void loop() {
  
  if(Serial.available()) {
    
    serialIn = Serial.readString();
    delay(10);
    
    if(serialIn == LEFT_COMMAND){
      servoDirectionRight = false;
      servoTimes = SERVO_MAX_TIMES;
      sendPosition = true;
    }
    if(serialIn == RIGHT_COMMAND){
      servoDirectionRight = true;
      servoTimes = SERVO_MAX_TIMES;
      sendPosition = true;
    }
    if(serialIn == STOP_COMMAND){
      servoTimes = -1000;
      sendPosition = true;
    }
    
  } else {
    if(sendPosition){
      sendPosition = false;
      Serial.print(servoPosition);
    }    
  }

  
  if(servoTimes > 0){
    servoTimes--;
    changeServoPosition( servoDirectionRight ? SERVO_SPEED : -SERVO_SPEED );
    controlledServo.write(servoPosition);    
  }

  delay(SERVO_DELAY);
}

void changeServoPosition(int delta){
  servoPosition += delta;
  if(servoPosition < MIN_ANGLE) servoPosition = MIN_ANGLE;
  if(servoPosition > MAX_ANGLE) servoPosition = MAX_ANGLE;
}

