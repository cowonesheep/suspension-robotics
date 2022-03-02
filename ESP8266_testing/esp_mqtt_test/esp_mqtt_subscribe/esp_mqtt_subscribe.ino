/*
 * ESP8266 (Adafruit HUZZAH) Mosquitto MQTT Subscribe Example
 * Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
 * Made as part of my MQTT Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
 */
#include <ESP8266WiFi.h> // Enables the ESP8266 to connect to the local network (via WiFi)
#include <PubSubClient.h> // Allows us to connect to, and publish to the MQTT broker

// Helper macro to merge bytes
#define TO_INT16(a,b) (((b)<<8)|(a))
#define TO_INT32(a,b,c,d) (((d)<<24)|((c)<<16)|((b)<<8)|(a))

const int ledPin = 0; // This code uses the built-in led for visual feedback that a message has been received

// WiFi
// Make sure to update this for your own WiFi network!
const char* ssid = "Your SSID";
const char* wifi_password = "Your WiFi Password";

// MQTT
// Make sure to update this for your own MQTT Broker!
const char* mqtt_server = "Your MQTT Server IP Address";
const char* mqtt_topic = "Your MQTT Topic";
// The client id identifies the ESP8266 device. 
const char* clientID = "ESP8266_1";

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, 1883, wifiClient); // 1883 is the listener port for the Broker

// Given an array of bytes, converts to integers and stores in converted[]
// Assumes byteArry is of size 32 and that two adjacent bytes represent an int
void readInt(byte* byteArray, int converted[], unsigned int length)
{
  int byteNum = 0;
  byte result[2];
  for (int i = 0; i < (length / 2); i++) {
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

void ReceivedMessage(char* topic, byte* payload, unsigned int length) {
  // Convert the payload to an integer array
  int convertedMessage[length / 2];
  readInt(payload, convertedMessage, length);

  int expectedMessage[] = {1, 2, 3, 4, 5, 6};
  int expectedSize = 6;
  // Handle the message we received
  if (intArraysEqual(convertedMessage, length / 2, expectedMessage, expectedSize)) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
  
//  // Here, we are only looking at the first character of the received message (payload[0])
//  // If it is 0, turn the led off.
//  // If it is 1, turn the led on.
//  if ((char)payload[0] == '0') {
//    digitalWrite(ledPin, HIGH); // Notice for the HUZZAH Pin 0, HIGH is OFF and LOW is ON. Normally it is the other way around.
//  }
//  if ((char)payload[0] == '1') {
//    digitalWrite(ledPin, LOW);
//  }
}

bool Connect() {
  // Connect to MQTT Server and subscribe to the topic
//  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    if (client.connect(clientID)) {
      client.subscribe(mqtt_topic);
      return true;
    }
    else {
      return false;
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);

  // Switch the on-board LED off to start with
  digitalWrite(ledPin, HIGH);

  // Begin Serial on 115200
  // Remember to choose the correct Baudrate on the Serial monitor!
  // This is just for debugging purposes
  Serial.begin(115200);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // setCallback sets the function to be called when a message is received.
  client.setCallback(ReceivedMessage);
  if (Connect()) {
    Serial.println("Connected Successfully to MQTT Broker!");  
  }
  else {
    Serial.println("Connection Failed!");
  }
}

void loop() {
  // If the connection is lost, try to connect again
  if (!client.connected()) {
    Connect();
  }
  // client.loop() just tells the MQTT client code to do what it needs to do itself (i.e. check for messages, etc.)
  client.loop();
  // Once it has done all it needs to do for this cycle, go back to checking if we are still connected.
}
