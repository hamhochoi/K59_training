//    #define KEY 7 
//    #define LED 13
//    
//    bool ok;
//    int var;
//    String bf = "";
//
//    bool configure_HC05();
//    
//    void setup()
//    {
//     pinMode(KEY, OUTPUT);
//     digitalWrite(KEY, HIGH);     
//     pinMode(LED, OUTPUT);
//     digitalWrite(LED, LOW);  
//     delay(3000);     
//     Serial.begin(9600);     
//     //ok = configure_HC05();
//    }
//     
//    void loop() {
//      if (ok)
//      {
////       Serial.println("ok");
//       if (Serial.available() > 0)
//       {
////        Serial.println("available");
//        var = Serial.read();
//        Serial.println(var);
//        if (var == 1) {
//         digitalWrite(LED, HIGH);
//        } else if (var == 0) {
//         digitalWrite(LED, LOW);
//        }
//       }
//      }
//    }
//    bool configure_HC05(){
//    
//        digitalWrite(KEY, HIGH);
//        
//        Serial.println("AT");
//        delay(2000);
//        if (!Serial.find("OK")){
//           return false;
//        }
//
////        Serial.println("AT+RMAAD");
////        delay(2000);
////        if (!Serial.find("OK")){
////         return false;
////        }
//        
////        Serial.println("AT+PSWD=1234");
////        delay(2000);
////        if (!Serial.find("OK")){
////         return false;
////        }
////        Serial.println("OK PSWD");
//
////        Serial.println("AT+ROLE=0");
////        delay(2000);
////        if (!Serial.find("OK")){
////         return false;
////        }
//        digitalWrite(KEY, LOW);
//        Serial.println("write KEY to LOW");
////        Serial.println("AT+RESET");
////        delay(2000);
////        if (!Serial.find("OK")){
////         return false;
////        }
//        
//        delay(5000);     
//        Serial.println("Bluetooth Ready!");
//        
//        return true;
//       }

//void setup(){}
//void loop(){}









// Code cho arduino thu 2

// Basic bluetooth test sketch. HC-06_01
// HC-06 ZS-040 
// 
// 
//  Uses hardware serial to talk to the host computer and software serial for communication with the bluetooth module
//
//  Pins
//  BT VCC to Arduino 5V out. 
//  BT GND to GND
//  BT RX to Arduino pin 11 (through a voltage divider)
//  BT TX  to Arduino pin 10 (no need voltage divider)
//
//  When a command is entered in the serial monitor on the computer 
//  the Arduino will relay it to the bluetooth module and display the result.
//
//  These HC-06 modules require capital letters and no line ending
//
 
#include <SoftwareSerial.h>
SoftwareSerial BTSerial(10, 11); // RX | TX
 
void setup() 
{
  Serial.begin(9600);
  Serial.print("Enter AT commands:");
 
  // HC-06 default baud rate is 9600
  BTSerial.begin(9600);  
}
 
void loop()
{
 
  // Keep reading from HC-06 and send to Arduino Serial Monitor
  if (BTSerial.available())
    Serial.write(BTSerial.read());
 
  // Keep reading from Arduino Serial Monitor and send to HC-06
  if (Serial.available())
    BTSerial.write(Serial.read());
}

//int ledPin = 13;
// 
//void setup() {
//  Serial.begin( 9600 );    // 9600 is the default baud rate for the serial Bluetooth module
//}
// 
//void loop() {
//  // listen for the data
//  if ( Serial.available() > 0 ) {
//    // read a numbers from serial port
//    int count = Serial.parseInt();
//    
//     // print out the received number
//    if (count > 0) {
//        Serial.print("You have input: ");
//        Serial.println(String(count));
//        // blink the LED
//        blinkLED(count);
//    }
//  }
//}
// 
//void blinkLED(int count) {
//  for (int i=0; i< count; i++) {
//    digitalWrite(ledPin, HIGH);
//    delay(500);
//    digitalWrite(ledPin, LOW);
//    delay(500);
//  } 
//}

