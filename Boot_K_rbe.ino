#include <Servo.h>

int stl = 7;
int sbl = 6;
int ftl = 5;
int fbl = 4;
int mini = 80;
int maxi = 100;
int delaybetweentriggers = 50*1000;
Servo Seite;
Servo Vorne;

void setup() {
  Vorne.attach(9);
  Vorne.write(90);
  Seite.attach(8);
  Seite.write(90);
  pinMode(stl, INPUT_PULLUP);
  pinMode(sbl, INPUT_PULLUP);
  pinMode(ftl, INPUT_PULLUP);
  pinMode(fbl, INPUT_PULLUP);
}

void loop() {
  delay(delaybetweentriggers);
  while (digitalRead(stl)!=HIGH) {
    Seite.write(maxi);
  }
  delay(100);
  while (digitalRead(sbl)!=HIGH) {
    Seite.write(mini);
  }
  Seite.write(90);
  delay(delaybetweentriggers);
  while (digitalRead(ftl)!=HIGH) {
    Vorne.write(maxi);
  }
  delay(100);
  while (digitalRead(fbl)!=HIGH) {
    Vorne.write(mini);
  }
  Vorne.write(90);
}
