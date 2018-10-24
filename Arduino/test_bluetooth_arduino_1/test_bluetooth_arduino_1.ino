

// Basic Bluetooth sketch HC-05_AT_MODE_01
// Connect the HC-05 module and communicate using the serial monitor
//
// The HC-05 defaults to commincation mode when first powered on you will need to manually enter AT mode
// The default baud rate for AT mode is 38400
// See www.martyncurrey.com for details
//
 

#include <SoftwareSerial.h>
SoftwareSerial BTserial(10, 11); // RX | TX
// Connect the HC-05 TX to Arduino pin 10 RX. 
// Connect the HC-05 RX to Arduino pin 11 TX through a voltage divider.
// 
 
char c = ' ';
 
void setup() 
{
    Serial.begin(9600);
    Serial.println("Arduino is ready");
    Serial.println("Remember to select Both NL & CR in the serial monitor");
 
    // HC-05 default serial speed for AT mode is 38400
    //BTserial.begin(38400);
    BTserial.begin(9600);
      
}

int value = 0; 

void loop()
{
    BTserial.write(++value);
    // Keep reading from HC-05 and send to Arduino Serial Monitor
    if (BTserial.available())
    {  
        c = BTserial.read();
        Serial.write(c);
    }
 
    // Keep reading from Arduino Serial Monitor and send to HC-05
    if (Serial.available())
    {
        c =  Serial.read();
        BTserial.write(c);  
    }
} 











/// Code 2

//int ledPin = 13;
// 
//void setup() {
//  Serial.begin( 9600 );    // 9600 is the default baud rate for the serial Bluetooth module
//}
//
//int count = 0; 
//void loop() {
//  //Serial.println(count++);
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







/// Code 3

//#include <SoftwareSerial.h>
//SoftwareSerial BTSerial(10, 11); // RX | TX
//String character;
//
//void setup()
//{
//  Serial.begin(9600);
//  pinMode(9, OUTPUT);  // this pin will pull the HC-05 pin 34 (key pin) HIGH to switch module to AT mode
//  digitalWrite(9, HIGH);
//  Serial.println("Enter AT commands:");
//  BTSerial.begin(9600);  // HC-05 default speed in AT command more
//  BTSerial.println("Bluetooth");
//}
//
//void loop()
//{
//  if (BTSerial.available()) {
//    character = BTSerial.read();
//    Serial.println(character);
//    BTSerial.flush();
//  }
//}
