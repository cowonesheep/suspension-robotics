"""
Python MQTT Subscription client - No Username/Password
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""
import paho.mqtt.client as mqtt
import time

# Don't forget to change the variables for the MQTT broker!
mqtt_topic = "Your Topic"
mqtt_broker_ip = "Your Broker IP"

client = mqtt.Client()

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print("Connected!" + str(rc))
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    print("Topic: " + msg.topic + "\nMessage: " + str(msg.payload))
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

def on_publish(client, userdata, mid):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1

# Here, we are telling the client which functions are to be run
# on connecting, on receiving a message, and on publishing
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)

# Once we have told the client to connect, let the client object run itself
#client.loop_forever()
client.loop_start()
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
 
        value = raw_input('Enter the message:')
        result = client.publish(mqtt_topic,value)
        status = result[0]
        if status == 0:
             print(f"Send `{value}` to topic `{mqtt_topic}`")
         else:
             print(f"Failed to send message to topic {mqtt_topic}")
 
except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()
