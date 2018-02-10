#include <ESP8266WiFi.h>
#include "PubSubClient.h"
#include "ArduinoJson.h"
#include <SoftwareSerial.h>
#include <ArduinoOTA.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266HTTPUpdateServer.h>


const byte RX = D1;
const byte TX = D2;
 
SoftwareSerial mySerial = SoftwareSerial(RX, TX, false, 256); 

//#define mqtt_server "test.mosquitto.org"
#define mqtt_server "192.168.60.199"
#define mqtt_topic_pub "zone_3/box_1/light/id_1"
//#define mqtt_topic_sub "light/switch"
#define mqtt_topic_sub "zone_3/box_1/led"
#define mqtt_topic_check_status "light/status"


//IPAddress staticIP(192,168,60,175);   // Phong may
//IPAddress staticIP(192,168,60,171);   // Phong can bo
IPAddress staticIP(192,168,60,176);   // Phong ngoai

IPAddress gateway(192,168,60,1);
IPAddress subnet(255,255,255,0);

const char *ssid =  "HPCC_IOT";     /// replace with your wifi ssid and wpa2 key.
const char *pass =  "hpcc_iot";
//const char* ssid = "ThuyHuong";
//const char* pass = "09061994";
//const char* host = "esp8266-webupdate";

//ESP8266WebServer httpServer(80);
//ESP8266HTTPUpdateServer httpUpdater;

WiFiClient ESPclient;
PubSubClient client(ESPclient);

long lastMsg = 0;
char msg[50];
int value = 0;


//unsigned long time = 0;
void setup_wifi();
 
void setup() 
{
      Serial.begin(115200);
      mySerial.begin(115200);
      setup_wifi();
//      WiFi.mode(WIFI_STA);
      client.setServer(mqtt_server, 1883);
      client.setCallback(callback);
      pinMode(LED_BUILTIN, OUTPUT);
      digitalWrite(LED_BUILTIN, LOW);

//      MDNS.begin(host);
//
//      httpUpdater.setup(&httpServer);
//      httpServer.begin();
//    
//      MDNS.addService("http", "tcp", 80);
//      Serial.printf("HTTPUpdateServer ready! Open http://%s.local/update in your browser\n", host);
      
}

void setup_wifi(){
      delay(10);
      Serial.println("Connecting to ");
      Serial.println(ssid); 
     
      WiFi.begin(ssid, pass);
      WiFi.config(staticIP, gateway, subnet); 
      
      while (WiFi.status() != WL_CONNECTED) 
      {
        delay(500);
        Serial.print(".");
      }
      Serial.println("");
      Serial.println("WiFi connected"); 
      Serial.println("IP address: ");
      Serial.println(WiFi.localIP());
}

// Ham callback de nhan du lieu
void callback(char* topic, byte* payload, unsigned int length) {
      Serial.print("Message arrived [");
      Serial.print(topic);
      Serial.print("] ");
      
      if(strcmp(topic,mqtt_topic_sub)==0){
         payload[length] = '\0';  // Cắt bỏ dữ liệu thừa
         char inData[80];
         char payload_string[100];
         strncpy(payload_string, (char*)payload,sizeof(payload_string)); // chuyển về dàng char
         Serial.println(payload_string);
         mySerial.print(payload_string);
         client.publish(mqtt_topic_check_status, payload_string);
      }
      Serial.println();
}

void reconnect() {
      // Loop until we're reconnected
      while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        // Create a random client ID
        String clientId = "ESP8266Client-";
        clientId += String(random(0xffff), HEX);
        // Attempt to connect
        if (client.connect(clientId.c_str())) {
          Serial.println("connected");
          // Once connected, publish an announcement...
          //client.publish(mqtt_topic_pub, "hello world");
          // ... and resubscribe
          boolean boo = client.subscribe(mqtt_topic_sub);
          Serial.println(boo);
        } else {
          Serial.print("failed, rc=");
          Serial.print(client.state());
          Serial.println(" try again in 5 seconds");
          // Wait 5 seconds before retrying
          delay(5000);
        }
      }
}

// Nhan du lieu tu arduino va publish/subscribe len server 
int light=0;
int temperature = 0;
int humidity = 0;

StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_weather[200];

void loop() 
{      
//  httpServer.handleClient();
  // Kiem tra ket noi
  if (!client.connected()){
    reconnect();
  }
  
  client.loop();
  if(mySerial.available() > 0){
    light = mySerial.read();
    temperature = mySerial.read();
    humidity = mySerial.read();
    
//    Serial.println(light);
    long now = millis();
//    if (now - lastMsg > 100){
      lastMsg = now;
      
      json_buffer["light"] = light;
      json_buffer["temperature"] = temperature;
      json_buffer["humidity"] = humidity; 
      
      json_buffer.printTo(buffer_weather, sizeof(buffer_weather));
      Serial.println(buffer_weather);
      client.publish(mqtt_topic_pub, buffer_weather);

//    }
  }
  delay(1000);

}
