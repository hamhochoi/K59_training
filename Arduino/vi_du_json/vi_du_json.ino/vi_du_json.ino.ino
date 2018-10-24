#include "ArduinoJson.h"



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_weather = jsonBuffer.createObject();
char buffer_weather[200];

void loop() {
  // put your main code here, to run repeatedly:
  json_weather["montion"] = 1;
  json_weather.printTo(buffer_weather, sizeof(buffer_weather));
  Serial.println(buffer_weather);
  delay(1000);
}
