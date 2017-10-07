#include <Servo.h>
#include <Adafruit_PWMServoDriver.h>

const short SERIAL_BAUD_RATE = 9600;
const byte SERIAL_TIMEOUT = 20;

const short SERVOS_COUNT = 6;

const byte SG90_MIN = 120;
const short SG90_MAX = 540;
const byte MG995_MIN = 110;
const short MG995_MAX = 595;

const byte GET_SERVOS_POSITIONS_COMMAND_CODE = 255;
const byte WHEELS_COMMAND_CODE = 200;
const byte SERVOS_COMMAND_CODE = 100;
const byte SERVOS_COMMAND_ARGUMENTS_ADDRESS_OFFSET = 1;

//short servoPins[SERVOS_COUNT] = { 3, 5, 6, 9, 10, 11 };

short leftFwd = 8;
short leftBck = 7;
short rightFwd = 2;
short rightBck = 4;
short leftSpeedPin = 9;
short rightSpeedPin = 3;

Adafruit_PWMServoDriver pwmDriver = Adafruit_PWMServoDriver(0x40);
//Servo servos[SERVOS_COUNT];
byte servoPositions[SERVOS_COUNT];

bool requredToSendPositions = false;

void setup() {
  
  Serial.begin(SERIAL_BAUD_RATE);
  Serial.setTimeout(SERIAL_TIMEOUT);
  
  /*
  for(short i = 0; i < SERVOS_COUNT; i++){
    servos[i].attach(servoPins[i]);
  }*/

  pwmDriver.begin();
  pwmDriver.setPWMFreq(60);

  pinMode(leftFwd, OUTPUT);
  pinMode(leftBck, OUTPUT);
  pinMode(rightFwd, OUTPUT);
  pinMode(rightBck, OUTPUT);
  pinMode(leftSpeedPin, OUTPUT);
  pinMode(rightSpeedPin, OUTPUT);
}

void loop() {
  byte bytesAvaibleCount = (byte)Serial.available();
  byte currentServoArgumentNumber;
  if(bytesAvaibleCount) {
    Serial.readBytes(servoPositions, bytesAvaibleCount);

    switch(servoPositions[0]){
      case GET_SERVOS_POSITIONS_COMMAND_CODE:
        requredToSendPositions = true;
        break;
      case WHEELS_COMMAND_CODE:
        SetWheels(servoPositions[1], servoPositions[2], servoPositions[3]);
        break;
      case SERVOS_COMMAND_CODE:
        for(short i = 0; i < SERVOS_COUNT; i++){
          currentServoArgumentNumber = i + SERVOS_COMMAND_ARGUMENTS_ADDRESS_OFFSET;
          //if(currentServoArgumentNumber >= bytesAvaibleCount) break;
          pwmDriver.setPWM(i, 0, getSG90PulseFromDegree(servoPositions[currentServoArgumentNumber]));
        }
    }
  }
  /*else{
    if(requredToSendPositions){
      SetServosPositions();
      Serial.write(servoPositions, SERVOS_COUNT);
      requredToSendPositions = false;
    }
  }*/
}

/*void SetServosPositions(){
  for(byte i=0; i<SERVOS_COUNT; i++){
    servoPositions[i] = servos[i].read();
  }
}*/

void SetWheels(byte parameter, byte speedLeft, byte speedRight){
  SetWheels(parameter, rightFwd, rightBck);
  SetWheels(parameter>>2, leftFwd, leftBck);
  analogWrite(leftSpeedPin, speedLeft);
  analogWrite(rightSpeedPin, speedRight);
}

void SetWheels(byte parameter, short fwdPin, short bckPin){
  if((parameter&3) != 3){
    switch(parameter&3){
      case 0:
        //stop
        digitalWrite(fwdPin, LOW);
        digitalWrite(bckPin, LOW);
        break;
      case 1:
        //forward;
        digitalWrite(fwdPin, HIGH);
        digitalWrite(bckPin, LOW);
        break;
      case 2:
        //back
        digitalWrite(fwdPin, LOW);
        digitalWrite(bckPin, HIGH);
        break;        
    }
  }
}

short getSG90PulseFromDegree(byte position180based){
  return map(position180based, 0, 181, SG90_MIN, SG90_MAX);
}

short getMG995PulseFromDegree(byte position180based){
  return map(position180based, 0, 181, MG995_MIN, MG995_MAX);
}

