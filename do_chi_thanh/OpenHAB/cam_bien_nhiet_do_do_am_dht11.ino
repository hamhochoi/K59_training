#include <SoftwareSerial.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include "ArduinoJson.h"
    
SoftwareSerial mySerial(10, 11); // RX, TX

const int DHTPIN = 2;
const int DHTTYPE = DHT11;  // Khai bao loai cam bien, co 2 loai la DHT11 va DHT22
DHT dht(DHTPIN, DHTTYPE);
    

int ledXanh = 3;        // chọn chân 13 báo hiệu LED
int ledDo = 4; 
int ledVang = 5; 

void setup(){
  Serial.begin(9600);
  mySerial.begin(115200);
}


int temperature = 0;
int humidity = 0;
    
StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_temp[200];
   
void loop()
{
      
      float h = dht.readHumidity(); //Doc do am
      float t = dht.readTemperature(); // Doc nhiet do
      Serial.print("Nhiet do: ");
      Serial.println(t);
      Serial.print("Do am: ");
      Serial.println(h);

     json_buffer["temperature"] = t;
     json_buffer["humidity"] = h;

     json_buffer.printTo(buffer_temp, sizeof(buffer_temp));
      
     mySerial.write(t);    // Gui cho esp8266
     mySerial.write(h);       // Gui cho esp8266
     mySerial.write(buffer_temp);
     Serial.println();
     delay(10);
      
}
   
