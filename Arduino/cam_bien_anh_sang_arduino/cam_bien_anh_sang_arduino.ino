#include <SoftwareSerial.h>
#include <DHT.h>
#include <Adafruit_Sensor.h>
#include <ArduinoJson.h>

SoftwareSerial mySerial(10, 11); // RX, TX

const int DHTPIN = 2;
const int DHTTYPE = DHT11;  // Khai bao loai cam bien, co 2 loai la DHT11 va DHT22
DHT dht(DHTPIN, DHTTYPE);
const int LDR_Pin = A0;
//int BATTERY = A1;

void setup() {
  Serial.begin(115200);
  mySerial.begin(115200);
//  pinMode(BATTERY, INPUT);
}

StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_temp[200];

int LDRReading = 0;
int temperature = 0;
int humidity = 0;
//int battery = 0;
void loop()
{
  LDRReading = analogRead(LDR_Pin);
//  battery = analogRead(BATTERY);

//  Serial.println(BATTERY);
  Serial.println(LDRReading);

  if (LDRReading < 500) {
    LDRReading = 0;
  }
  else if (LDRReading >= 500 && LDRReading < 900) {
    LDRReading = 1;
  }
  else {
    LDRReading = 2;
  }



  humidity = dht.readHumidity(); //Doc do am
  temperature = dht.readTemperature(); // Doc nhiet do
  Serial.print("Nhiet do: ");
  Serial.println(temperature);
  Serial.print("Do am: ");
  Serial.println(humidity);
  Serial.println();

  json_buffer["light"] = LDRReading;
  json_buffer["temperature"] = temperature;
  json_buffer["humidity"] = humidity;
//  json_buffer["battery"] = battery;


  json_buffer.printTo(buffer_temp, sizeof(buffer_temp));
  Serial.println(buffer_temp);
  //      mySerial.write(temp_str); // Gui cho Esp8266
  //      mySerial.write(hum_str);
  //      mySerial.write(light_str);
  mySerial.write(buffer_temp);

  delay(2500);

}

