#include <ESP8266WiFi.h>
#include "PubSubClient.h"
#include "ArduinoJson.h"
#include <SoftwareSerial.h>
const byte RX = D1;
const byte TX = D2;

SoftwareSerial mySerial = SoftwareSerial(RX, TX, false, 256);

//#define mqtt_server "broker.hivemq.com"
#define mqtt_server "192.168.0.197"
#define mqtt_topic_pub "zone_3/box_1/motion/id_1"
#define mqtt_topic_sub "zone_3/box_1/led"
#define mqtt_topic_check_status "light/status"

//IPAddress staticIP(192,168,0,174); // Phong may
IPAddress staticIP(192, 168, 0, 173); // Phong ngoai
//IPAddress staticIP(192,168,0,172); // Phong can bo

IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);
//
const char *ssid =  "HPCC_IOT";     /// replace with your wifi ssid and wpa2 key./
const char *pass =  "hpcc_iot";


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
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void setup_wifi() {
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

  if (strcmp(topic, mqtt_topic_sub) == 0) {
    payload[length] = '\0';  // Cắt bỏ dữ liệu thừa
    char inData[80];
    char payload_string[100];
    strncpy(payload_string, (char*)payload, sizeof(payload_string)); // chuyển về dàng char
    Serial.println(payload_string);
    mySerial.print(payload_string);
    client.publish(mqtt_topic_check_status, payload_string);
  }
  Serial.println();
  delay(100);
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
      client.subscribe(mqtt_topic_sub);
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
int motion = 0;
int battery = 0;
StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_motion[200];
char ledDo[10];
char ledXanh[10];
char ledVang[10];

void loop()
{
  // Kiem tra ket noi
  if (!client.connected()) {
    reconnect();
  }

  client.loop();
  if (mySerial.available() > 0) {
    motion = mySerial.read();
    //    ledDo = mySerial.read();
    //    ledVang = mySerial.read();
    //    ledXanh = mySerial.read();
    //
    //    battery = mySerial.read();
    long now = millis();
    if (now - lastMsg > 100) {
      lastMsg = now;

      json_buffer["motion"] = motion;
      //      json_buffer["LedXanh"] = ledXanh;
      //      json_buffer["LedDo"] = ledDo;
      //      json_buffer["LedVang"] = ledVang;
      //
      //      json_buffer["battery"] = battery;
      json_buffer.printTo(buffer_motion, sizeof(buffer_motion));
      Serial.println(buffer_motion);
      client.publish(mqtt_topic_pub, buffer_motion);

    }
  }

  delay(100);

}

