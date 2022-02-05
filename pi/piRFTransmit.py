import RPi.GPIO as GPIO  # import gpio
import time      #import time library
import spidev
import struct
from lib_nrf24 import NRF24   #import NRF24 library

# Given an integer array, converts to bytes
# Note: since Arduino has 2 byte ints and python has 4,
#       using python's short representation
def int_array_to_bytes(int_array):
    return struct.pack("h"*len(int_array),*int_array)

# After keyboard input, returns a test array of integers [0,15]
def get_int_array():

    inp = input('Test format: [g/b for good or bad][# arduino]')
    if (len(inp) != 2 or (inp[0] != 'g' and inp[0] != 'b') or (not inp[1].isnumeric())):
        #bad input
        return [0 for n in range(40)]
    array = [1, 244, 355, 66, 123, -90, -100, 10, 3, 0, 0, 0, 0, 0, 0, 0]
    if inp[0] == 'b':
        array[2] = 4;#replace an int
    array[0] = int(inp[1])
    return array

# Gets message in characters and fills remaining with 0s
def get_message():
    inp = input('Message to send: ')
    sendMessage = list(inp)  #the message to be sent
    while len(sendMessage) < 32:    
        sendMessage.append(0)
    return sendMessage

GPIO.setmode(GPIO.BCM)       # set the gpio mode

  # set the pipe address. this address shoeld be entered on the receiver alo
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]
radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins
radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25
radio.setPayloadSize(32)  #set the payload size as 32 bytes
radio.setChannel(0x76) # set the channel as 76 hex
radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate
radio.setPALevel(NRF24.PA_MIN)  # set PA level

radio.setAutoAck(True)       # set acknowledgement as true 
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[0])     # open the defined pipe for writing
radio.printDetails()      # print basic detals of radio

while True:
    #get our integers and convert to bytes before sending
    integer_array = get_int_array()
    sendMessage = int_array_to_bytes(integer_array)
    print(len(sendMessage))
    #prevent sending messages longer than 32 bytes
    if (len(sendMessage) > 32):
        print("Can't send message longer than 32 bytes")
        continue
    start = time.time()      #start the time for checking delivery time
    radio.write(sendMessage)   # just write the message to radio
    print("Sent the message: {}".format(sendMessage))  # print a message after succesfull send
    radio.startListening()        # Start listening the radio
    
    while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start > 2:
            print("Timed out.")  # print errror message if radio disconnected or not functioning anymore
            break

    radio.stopListening()     # close radio
    time.sleep(3)  # give delay of 3 seconds

