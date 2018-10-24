#include <ESP8266WiFi.h>
#include "PubSubClient.h"
#include "ArduinoJson.h"
#include <SoftwareSerial.h>
const byte RX = D1;
const byte TX = D2;
 
SoftwareSerial mySerial = SoftwareSerial(RX, TX, false, 256); 

//#define mqtt_server "test.mosquitto.org"
#define mqtt_server "192.168.0.198"
#define mqtt_topic_pub "v1/devices/me/telemetry"
#define mqtt_topic_sub "v1/devices/me/rpc/request/+"

#define GPIO3_PIN 3
#define GPIO4_PIN 4
#define GPIO5_PIN 5

//IPAddress staticIP(192,168,60,174); // Phong may
//IPAddress staticIP(192,168,60,173); // Phong ngoai
IPAddress staticIP(192,168,0,172); // Phong can bo

IPAddress gateway(192,168,0,1);
IPAddress subnet(255,255,255,0);

const char *ssid =  "HPCC_IOT";     /// replace with your wifi ssid and wpa2 key./
const char *pass =  "hpcc_iot"; 
//const char* ssid = "ThuyHuong";
//const char* pass = "09061994";

WiFiClient ESPclient;
PubSubClient client(ESPclient);

long lastMsg = 0;
char msg[50];
int value = 0;
boolean gpioState[] = {false, false, false};


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
  
//  if(strcmp(topic,mqtt_topic_sub)==0){/
     payload[length] = '\0';  // Cắt bỏ dữ liệu thừa
     char inData[80];
     char payload_string[100];
     strncpy(payload_string, (char*)payload,sizeof(payload_string)); // chuyển về dàng char
     Serial.println(payload_string);

      // Decode JSON request
      StaticJsonBuffer<200> jsonBuffer;
      JsonObject& data = jsonBuffer.parseObject((char*)payload_string);
    
      if (!data.success())
      {
        Serial.println("parseObject() failed");
        return;
      }
    
      // Check request method
      String methodName = String((const char*)data["method"]);
    
      if (methodName.equals("getGpioStatus")) {
        // Reply with GPIO status
        String responseTopic = String(topic);
        responseTopic.replace("request", "response");
        client.publish(responseTopic.c_str(), get_gpio_status().c_str());
//        Serial.print("{\"3\": \"false\"}");
//        client.publish(responseTopic.c_str(), "{\"3\": \"false\"}");
      } else if (methodName.equals("setGpioStatus")) {
          set_gpio_status(data["params"]["pin"], data["params"]["enabled"]);

//          boolean command_xanh = boolean(data["params"]["xanh"]);
//          boolean command_do = boolean(data["params"]["do"]);
//          boolean command_vang = boolean(data["params"]["vang"]);
//          String command_to_arduino, state;
//          String led_xanh, led_do, led_vang;
//          
//      if (command_xanh == true){
//        led_xanh = "ON";
//        state = "{\"3\": \"true\"}";
//      } else if (command_xanh == false){
//          led_xanh = "OFF";
//          state = "{\"3\": \"false\"}";
//      } else{
//        Serial.print("loi den xanh!");
//      }
//      command_to_arduino = "{\"xanh\" :" + String("\"") + String(led_xanh) + "\"}";
//      set_gpio_status(command_to_arduino);
      
      // Update GPIO status and reply
      String responseTopic = String(topic);
      responseTopic.replace("request", "response");
      Serial.print(responseTopic);

//      client.publish(responseTopic.c_str(), command_to_arduino.c_str());
      client.publish(responseTopic.c_str(), get_gpio_status().c_str());
      client.publish("v1/devices/me/telemetry", get_gpio_status().c_str());

//      Serial.print(state);

//        client.publish("v1/devices/me/attributes", get_gpio_status().c_str());
      }


     
//     mySerial.print(payload_string);
//  }/
  Serial.println();
  delay(100);
}



String get_gpio_status() {
  // Prepare gpios JSON payload string
  StaticJsonBuffer<200> jsonBuffer;
  JsonObject& data = jsonBuffer.createObject();
  data[String(GPIO3_PIN)] = gpioState[0] ? true : false;
  data[String(GPIO4_PIN)] = gpioState[1] ? true : false;
  data[String(GPIO5_PIN)] = gpioState[2] ? true : false;
  char payload[256];
  data.printTo(payload, sizeof(payload));
  String strPayload = String(payload);
  Serial.print("Get gpio status: ");
  Serial.println(strPayload);
  return strPayload;
}

void set_gpio_status(int pin, boolean enabled) {
//  boolean command_xanh = boolean(data["params"]["enabled"]);
//  boolean command_do = boolean(data["params"]["enabled"]);
//  boolean command_vang = boolean(data["params"]["enabled"]);
  String command_to_arduino;
  String led_xanh, led_do, led_vang;

  if(pin == 3){
    if (enabled == true){
      led_xanh = "ON";
    } else if (enabled == false){
        led_xanh = "OFF";
    } else{
      Serial.print("loi den xanh!");
    }
    command_to_arduino = "{\"xanh\" :" + String("\"") + String(led_xanh) + "\"}";
    gpioState[0] = enabled;
    mySerial.print(command_to_arduino);
  } else if (pin == 4) {
    if (enabled == true){
      led_do = "ON";
      } else if (enabled == false){
          led_do = "OFF";
      } else{
          Serial.print("loi den do!");
      }
      command_to_arduino = "{\"do\" :" + String("\"") + String(led_do) + "\"}";
      gpioState[1] = enabled;
      mySerial.print(command_to_arduino);
  } else if (pin == 5) {
      if (enabled == true){
        led_vang = "ON";
      } else if (enabled == false){
          led_vang = "OFF";
      } else{
          Serial.print("loi den vang!");
      }
      command_to_arduino = "{\"vang\" :" + String("\"") + String(led_vang) + "\"}";
      gpioState[2] = enabled;
      mySerial.print(command_to_arduino);
  }
}



void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    // hpcc_e99fdf20 (192.168.60.198)
    // TmGSjEMg8MqulNxAhVei (192.168.60.247)
    if (client.connect(clientId.c_str(), "HPCC_Motion_Led", NULL)) {
      Serial.println("connected");
      client.subscribe(mqtt_topic_sub);
      Serial.println("Sending current GPIO status ...");
//      client.publish("v1/devices/me/attributes", get_gpio_status()/.c_str());
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
StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_motion[200];

void loop() 
{      
  // Kiem tra ket noi
  if (!client.connected()){
    reconnect();
  }
  
  client.loop();
  if(mySerial.available() > 0){
    person = mySerial.read();
    long now = millis();
    if (now - lastMsg > 100){
      lastMsg = now;
      
      json_buffer["motion"] = person;  
      json_buffer.printTo(buffer_motion, sizeof(buffer_motion));
      Serial.println(buffer_motion);
      client.publish(mqtt_topic_pub, buffer_motion);
      
    }
  }
  delay(300);

}
