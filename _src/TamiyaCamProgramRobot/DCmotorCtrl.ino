#include <Wire.h>
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 
Adafruit_DCMotor *myMotor = AFMS.getMotor(1);
Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);

int8_t  drive   = 0; //stop state
int8_t  drive2  = 0; //stop state
uint8_t gp     = false; 

void runM(){
  uint8_t t;

  if( drive == abs(drive) ){
    myMotor->run(FORWARD);
  }else{
    myMotor->run(BACKWARD);
  }
  if( drive2 == abs(drive2) ){
    myMotor2->run(FORWARD);
  }else{
    myMotor2->run(BACKWARD);
  }

  t=abs(drive) *2; myMotor->setSpeed(t);
  t=abs(drive2)*2; myMotor2->setSpeed(t);

  //myMotor->run(RELEASE);
  //myMotor2->run(RELEASE);
}

void setup() {
  Serial.begin(9600);
  AFMS.begin();
}

void loop() {
  uint8_t in = false;

  //Retrieve Gamepad info from Raspberry Pi
  if (Serial.available()>0) {
    in = Serial.read();
    Serial.flush();
    if( in ){
      Serial.write(drive);
      Serial.write(drive2);
      gp = in;
      in = false;
    }
  }
  
  //Calc. each DC motor speed
  // based on bit assignment of Gamepad.
  /*
  [bit assignment]
   FORWARD  -> 1000 0000 -> 0x80
   BACKWARD -> 0100 0000 -> 0x40
   LEFT     -> 0010 0000 -> 0x20
   RIGHT    -> 0001 0000 -> 0x10
   STOP     -> 0000 0001 -> 0x01

  [gamepad key assignment]
   a1 -->> -: forward, +:backward
   a2 -->> -: left,    +:right
   b6+b7-> FORCE STOP
  */
  if( gp & 0x80 ){ //FORWARD
    if( drive  < 127 ){ drive++; }
    if( drive2 < 127 ){ drive2++; }
  }
  if( gp & 0x40 ){ //BACKWARD
    if( drive  > -127 ){ drive--; }
    if( drive2 > -127 ){ drive2--; }
  }
  if( gp & 0x20 ){ //RIGHT
    if( drive  > -127 ){ drive--; }
    if( drive2 <  127 ){ drive2++; }
  }
  if( gp & 0x10 ){ //LEFT
    if( drive  <  127 ){ drive++; }
    if( drive2 > -127 ){ drive2--; }
  }
  if( gp & 0x01 ){ //FORCE STOP
    drive  = 0;
    drive2 = 0;
  }
  //and just RUN.
  runM();

  delay(5);
}
