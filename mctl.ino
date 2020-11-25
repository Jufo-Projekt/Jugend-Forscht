#include <Servo.h>
int mini=75;
int maxi=115;
Servo lmotor;
Servo rmotor;
int lspeed=90;
int rspeed=90;
void setup(){
  lmotor.attach(9);
  rmotor.attach(8);
  lmotor.write(90);
  rmotor.write(90);
  Serial.begin(9600);
}
void loop(){
  int avb=Serial.available();
  if (avb>0){
    char ch = Serial.read();
    if (ch==49){lspeed-=1;}
    if (ch==50){lspeed+=1;}
    if (ch==51){rspeed-=1;}
    if (ch==52){rspeed+=1;}
    if (rspeed>maxi){wc();}
    if (lspeed>maxi){wc();}
    if (rspeed<mini){wc();}
    if (lspeed<mini){wc();}
    rmotor.write(rspeed);
    lmotor.write(lspeed);
  }
  delay(50);
}
void wc(){
  while (lspeed>90){lspeed-=1;lmotor.write(lspeed);delay(10);}
  while (lspeed<90){lspeed+=1;lmotor.write(lspeed);delay(10);}
  while (rspeed>90){rspeed-=1;rmotor.write(rspeed);delay(10);}
  while (rspeed<90){rspeed+=1;rmotor.write(rspeed);delay(10);}
  while (true){
    delay(1000);
  }
}
