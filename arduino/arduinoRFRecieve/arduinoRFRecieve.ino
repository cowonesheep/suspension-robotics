#include<SPI.h>                   // spi library for connecting nrf
#include <Wire.h>                             // i2c libary fro 16x2 lcd display
#include<RF24.h>                  // nrf library


// Helper macro to merge bytes
#define TO_INT16(a,b) (((b)<<8)|(a))
#define TO_INT32(a,b,c,d) (((d)<<24)|((c)<<16)|((b)<<8)|(a))

RF24 radio(9, 10) ;  // ce, csn pins

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
  //sanity check
  if (! radio.isChipConnected()) {
    Serial.println("Warning: RF chip isn't connected!");
  }
}


void loop() {

  radio.startListening() ;        // start listening forever
  byte receivedMessage[32];   // set incmng message for 32 bytes
  int convertedMessage[16];
  
  if (radio.available()) {       // check if message is coming
    radio.read(receivedMessage, sizeof(receivedMessage));    // read the message and save

    Serial.print("Message size: ");
    Serial.println(sizeof(receivedMessage));

    readInt(receivedMessage, convertedMessage);
    
    Serial.print("Converted message: ");
    for (int i = 0; i < 16; i++) {
      Serial.print(convertedMessage[i]);
      Serial.print(",");
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
