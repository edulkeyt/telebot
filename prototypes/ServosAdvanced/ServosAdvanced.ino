#include <Servo.h>

const short SERIAL_BAUD_RATE = 9600;
const byte SERIAL_TIMEOUT = 20;

const short SERVOS_COUNT = 6;

const byte GET_SERVOS_POSITIONS_COMMAND_CODE = 255;

short servoPins[SERVOS_COUNT] = { 3, 5, 6, 9, 10, 11 };

Servo servos[SERVOS_COUNT];
byte servoPositions[SERVOS_COUNT];

bool requredToSendPositions = false;

void setup() {
  
  Serial.begin(SERIAL_BAUD_RATE);
  Serial.setTimeout(SERIAL_TIMEOUT);
  for(short i = 0; i < SERVOS_COUNT; i++){
    servos[i].attach(servoPins[i]);
  }
}

void loop() {
  
  if(Serial.available()) {
    Serial.readBytes(servoPositions, SERVOS_COUNT);

    if(servoPositions[0] == GET_SERVOS_POSITIONS_COMMAND_CODE){
      requredToSendPositions = true;
    }
    else{
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

