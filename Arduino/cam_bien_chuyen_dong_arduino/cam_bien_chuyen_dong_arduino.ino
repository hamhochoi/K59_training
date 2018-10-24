#include <SoftwareSerial.h>
#include <ArduinoJson.h>
SoftwareSerial mySerial(10, 11); // RX, TX

int ledXanh = 3;        // chọn chân 13 báo hiệu LED
int ledDo = 4; 
int ledVang = 5; 

int inputPin = 2;       // chọn ngõ tín hiệu vào cho cảm biến chuyển động
int val = 0;

void setup(){
  pinMode(ledXanh, OUTPUT);
  pinMode(ledDo, OUTPUT);
  pinMode(ledVang , OUTPUT);
  pinMode(inputPin, INPUT);
//  digitalWrite(ledXanh,HIGH);
//  digitalWrite(ledVang,HIGH);
//  digitalWrite(ledDo, HIGH);
  Serial.begin(9600);
  mySerial.begin(115200);
}


StaticJsonBuffer<200> jsonBuffer;
JsonObject& json_buffer = jsonBuffer.createObject();
char buffer_motion[200];

void loop(){
    val = digitalRead(inputPin);    // đọc giá trị đầu vào.

    if(mySerial.available() > 0){
        StaticJsonBuffer<200> jsonBufferLed;
        String ledString = mySerial.readString();
        Serial.println(ledString);

        int index=0, pre_index=0;
        int num_led=3;
        int i=0;
        String subLedString;

        // Tach tung json trong message
//        while (i<num_led){
            index = ledString.indexOf("}", index+1);
            subLedString = ledString.substring(pre_index, index+1);
            pre_index = index+1;
//            Serial.println(subLedString);
            JsonObject& ledJson = jsonBufferLed.parseObject(subLedString);   // Den xanh
            
            /* OpenHAB*/
            if(strcmp(ledJson["vang"],"ON")==0){
              digitalWrite(ledVang,HIGH);
              Serial.println("Vang ON");
            }
            else if (strcmp(ledJson["vang"], "OFF")==0){
              digitalWrite(ledVang,LOW);
              Serial.println("Vang OFF");
            }

            if(strcmp(ledJson["do"],"ON")==0){
              digitalWrite(ledDo,HIGH);
              Serial.println("Do ON");
            }
            else if (strcmp(ledJson["do"], "OFF")==0){
              digitalWrite(ledDo,LOW);
              Serial.println("Do OFF");
            }
     
            if(strcmp(ledJson["xanh"],"ON")==0){
              digitalWrite(ledXanh,HIGH);
              Serial.println("Xanh ON");
            }
            else if (strcmp(ledJson["xanh"], "OFF")==0){
              digitalWrite(ledXanh,LOW);
              Serial.println("xanh OFF");
            }

            //////////////////////////////////
            /* Home Assistant*/
            if(strcmp(ledJson["name"],"Green Light")==0){
              if (strcmp(ledJson["value"], "ON") == 0){
                  digitalWrite(ledXanh,HIGH);
                  Serial.println("Xanh On");
              }
              else{
                  digitalWrite(ledXanh,LOW);
                  Serial.println("Xanh OFF");
              }
            }
    
            if(strcmp(ledJson["name"],"Yellow Light")==0){
              if (strcmp(ledJson["value"], "ON") == 0){
                  digitalWrite(ledVang,HIGH);
                  Serial.println("Vang On");
              }
              else{
                  digitalWrite(ledVang,LOW);
                  Serial.println("Vang OFF");
              }
            }

           if(strcmp(ledJson["name"],"Red Light")==0){
              if (strcmp(ledJson["value"], "ON") == 0){
                  digitalWrite(ledDo,HIGH);
                  Serial.println("Do On");
              }
              else{
                  digitalWrite(ledDo,LOW);
                  Serial.println("Do OFF");
              }
            } 
//            i++;
//        }
    }

  json_buffer["motion"] = val;
  json_buffer["LedDo"] = digitalRead(ledDo);
  json_buffer["LedVang"] = digitalRead(ledVang);
  json_buffer["LedXanh"] = digitalRead(ledXanh);  

  json_buffer.printTo(buffer_motion, sizeof(buffer_motion));
  Serial.println(buffer_motion);
  mySerial.write(val);
//  mySerial.write(digitalRead(ledDo));
//  mySerial.write(digitalRead(ledVang));
//  mySerial.write(digitalRead(ledXanh));
  delay(200);


}

