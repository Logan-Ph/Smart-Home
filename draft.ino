#include <Servo.h>
Servo servo1;
Servo servo2;

int bed_room_light = 8;
int toilet_light = 7;
int data;

void setup() {
  pinMode(bed_room_light, OUTPUT);
  pinMode(toilet_light, OUTPUT);
  servo1.attach(2);
  servo2.attach(4);
  Serial.begin(9600);
}

void loop() {
  while (Serial.available()) {
    data = Serial.read();
    
    if (data == '1') {
      digitalWrite(bed_room_light, HIGH);
    }
    else if (data == '0') {
      digitalWrite(bed_room_light, LOW); 
    }
    else if (data =='2') {
      digitalWrite(toilet_light,HIGH);
    }
    else if (data == '3') {
      digitalWrite(toilet_light,LOW);
    }
    else if (data == '4') {
      servo1.write(90);
      servo2.write(90);
      delay(500);
    }
    else if (data == '5') {
      servo1.write(0);
      servo2.write(0);
      delay(500);
    }
  }
}
