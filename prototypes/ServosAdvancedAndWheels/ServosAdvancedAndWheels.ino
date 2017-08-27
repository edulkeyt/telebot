#include <Servo.h>

const short SERIAL_BAUD_RATE = 9600;
const byte SERIAL_TIMEOUT = 20;

const short SERVOS_COUNT = 6;

const byte GET_SERVOS_POSITIONS_COMMAND_CODE = 255;

const byte WHEELS_COMMAND_CODE = 200;

short servoPins[SERVOS_COUNT] = { 3, 5, 6, 9, 10, 11 };

//short wheelPins[4] = { 2, 4, 7, 8 };
short leftFwd = 8;
short leftBck = 7;
short rightFwd = 2;
short rightBck = 4;

Servo servos[SERVOS_COUNT];
byte servoPositions[SERVOS_COUNT];

bool requredToSendPositions = false;

void setup() {
  
  Serial.begin(SERIAL_BAUD_RATE);
  Serial.setTimeout(SERIAL_TIMEOUT);
  for(short i = 0; i < SERVOS_COUNT; i++){
    servos[i].attach(servoPins[i]);
  }

  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  
  if(Serial.available()) {
    Serial.readBytes(servoPositions, SERVOS_COUNT);

    switch(servoPositions[0]){
      case GET_SERVOS_POSITIONS_COMMAND_CODE:
        requredToSendPositions = true;
        break;
      case WHEELS_COMMAND_CODE:
        SetWheels(servoPositions[1]);
        break;
      default:
        for(short i = 0; i < SERVOS_COUNT; i++){
          servos[i].write(servoPositions[i]);
        }
    }
  }
  else{
    if(requredToSendPositions){
      SetServosPositions();
      Serial.write(servoPositions, SERVOS_COUNT);
      requredToSendPositions = false;
    }
  }
}

void SetServosPositions(){
  for(byte i=0; i<SERVOS_COUNT; i++){
    servoPositions[i] = servos[i].read();
  }
}

void SetWheels(byte parameter){
  SetWheels(parameter, rightFwd, rightBck);
  SetWheels(parameter>>2, leftFwd, leftBck);
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

