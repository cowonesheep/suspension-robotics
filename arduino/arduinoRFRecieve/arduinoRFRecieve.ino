#include<SPI.h>                   // spi library for connecting nrf
#include <Wire.h>                             // i2c libary fro 16x2 lcd display
#include<RF24.h>                  // nrf library

// Arduino identifier
#define ME 1
// Helper macro to merge bytes
#define TO_INT16(a,b) (((b)<<8)|(a))
#define TO_INT32(a,b,c,d) (((d)<<24)|((c)<<16)|((b)<<8)|(a))

RF24 radio(9, 10) ;  // ce, csn pins

//RGB LEDs are connected to these pins
int RedPin = 3;
int GreenPin = 5;
int BluePin = 6;

void setup() {
  while (!Serial) ;
  Serial.begin(9600) ;     // start serial monitor baud rate
  Serial.println("Starting.. Setting Up.. Radio on..") ; // debug message
  radio.begin();        // start radio at ce csn pin 9 and 10
  radio.setPALevel(RF24_PA_MAX) ;   // set power level
  radio.setChannel(0x76) ;            // set chanel at 76
  const uint64_t pipe = 0xE0E0F1F1E0LL ;    // pipe address same as sender i.e. raspberry pi
  radio.openReadingPipe(1, pipe) ;        // start reading pipe
  radio.enableDynamicPayloads() ;
  radio.powerUp() ;
  Wire.begin();                 //start i2c address
  if (! radio.isChipConnected()) { //sanity check
    Serial.println("Warning: RF chip isn't connected!");
  }

  //set the LED pins to output
  pinMode(RedPin, OUTPUT);
  pinMode(GreenPin, OUTPUT);
  pinMode(BluePin, OUTPUT);
}


void loop() {

  radio.startListening() ;        // start listening forever
  byte receivedMessage[32];   // set incmng message for 32 bytes
  int convertedMessage[16];

  int testExpected[] = {ME, 244, 355, 66, 123, -90, -100, 10, 3, 0, 0, 0, 0, 0, 0, 0};

  if (radio.available()) {       // check if message is coming
    radio.read(receivedMessage, sizeof(receivedMessage));    // read the message and save

    readInt(receivedMessage, convertedMessage); //read the bytes and convert to int array

    //print the converted array
    Serial.print("Converted message: ");
    for (int i = 0; i < 16; i++) {
      Serial.print(convertedMessage[i]);
      Serial.print(" ");
    }

    /* 
     * testing: LED statuses based on converted array
     * green - message is intended for this arduino and matches expected
     * red   - message is intended for this arduino and doesn't match expected
     * yellow- message is not intended for this arduino
     */
    if (messageForMe(convertedMessage)) {
      if (intArraysEqual(testExpected, 16, convertedMessage, 16)) {
        Serial.println("Message for me and expected.");
        green();
      } else {
        Serial.println("Message for me and not expected.");
        red();
      }
    } else {
      Serial.println("Message not for me");
      yellow();
    }

    Serial.println("Turning off the radio.") ;   // print message on serial monitor
    radio.stopListening() ;   // stop listening radio
  }
  delay(10);
}

// Given an array of bytes, converts to integers and stores in converted[]
// Assumes byteArry is of size 32 and that two adjacent bytes represent an int
void readInt(byte byteArray[], int converted[])
{
  int byteNum = 0;
  byte result[2];
  for (int i = 0; i < 16; i++) {
    for (int j = 0; j < 2; j++) {
      result[j] = byteArray[byteNum];
      byteNum++;
    }
    converted[i] = TO_INT16(result[0], result[1]);
  }
}

// Given two integer arrays and ints representing their lengths,
// determines if the arrays are equal (in length and sequentially)
bool intArraysEqual(int array1[], int length1, int array2[], int length2)
{
  //  if (sizeof(array1) != sizeof(array2)) {
  if (length1 != length2) {
    return false;
  }
  for (int i = 0; i < length1; i++) {
    if (array1[i] != array2[i]) {
      return false;
    }
  }
  return true;
}

void red () {

  //set the LED pins to values that make red
  analogWrite(RedPin, 100);
  analogWrite(GreenPin, 0);
  analogWrite(BluePin, 0);
}

void green () {

  //set the LED pins to values that make green
  analogWrite(RedPin, 0);
  analogWrite(GreenPin, 100);
  analogWrite(BluePin, 0);
}

void yellow () {

  //set the LED pins to values that make yellow
  analogWrite(RedPin, 80);
  analogWrite(GreenPin, 30);
  analogWrite(BluePin, 0);
}

// Given an integer message, determines if the message is meant for this arduino
bool messageForMe(int message[]) {
  return message[0] == ME;
}
