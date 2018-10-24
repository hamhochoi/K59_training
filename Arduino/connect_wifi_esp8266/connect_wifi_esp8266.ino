#include <ESP8266WiFi.h>
#include "PubSubClient.h"

//#define mqtt_server "test.mosquitto.org"
#define mqtt_server "192.168.60.199"
#define mqtt_topic_pub "zone_1/box_1/temperature_humidity/id_1"
#define mqtt_topic_sub "zone_1/box_1/temperature_humidity/id_1"

IPAddress staticIP(192,168,60,170);
IPAddress gateway(192,168,60,1);
IPAddress subnet(255,255,255,0);

const char *ssid =  "HPCC_IOT";     // replace with your wifi ssid and wpa2 key
const char *pass =  "hpcc_iot";
//const char* ssid = "ThuyHuong";
//const char* pass = "09061994";

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
      setup_wifi();
      client.setServer(mqtt_server, 1883);
      client.setCallback(callback);
      pinMode(LED_BUILTIN, OUTPUT);
      digitalWrite(LED_BUILTIN, LOW);
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
  Serial.println("IPu address: ");
  Serial.println(WiFi.localIP());
}

// Ham callback de nhan du lieu
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
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
      client.publish(mqtt_topic_pub, "hello world");
      // ... and resubscribe
      //client.subscribe(mqtt_topic_sub);
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
int person = 0;


void loop() 
{      
  // Kiem tra ket noi
  if (!client.connected()){
    reconnect();
  }
  client.loop();
  
  if(Serial.available() > 0){
    person = Serial.read();
    long now = millis();
    if (now - lastMsg > 2000){
      lastMsg = now;
      //++value;
      snprintf(msg, 75, "motion: %d ", person);
      Serial.print("Publish message: ");
      Serial.println(person);
      client.publish(mqtt_topic_pub, msg);

    }
  }
  delay(2000);
}
