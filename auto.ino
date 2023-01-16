/*!
 * @file readDHT11.ino
 * @brief DHT11 is used to read the temperature and humidity of the current environment. 
 *
 * @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license     The MIT License (MIT)
 * @author [Wuxiao](xiao.wu@dfrobot.com)
 * @version  V1.0
 * @date  2018-09-14
 * @url https://github.com/DFRobot/DFRobot_DHT11
 */

#include <DFRobot_DHT11.h>
DFRobot_DHT11 DHT;
#define DHT11_PIN 7
int LED = 12;

void setup(){
  pinMode(LED,OUTPUT);
  Serial.begin(9600);
}

void loop(){
  DHT.read(DHT11_PIN);

  if (DHT.temperature >=32 && DHT.humidity > 70){
      digitalWrite(LED,HIGH);
    }
  else{
    digitalWrite(LED,LOW);
  }
 
  delay(1000);
}
