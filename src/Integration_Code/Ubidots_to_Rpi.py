'''
Sends data to Ubidots using MQTT
Example provided by Jose Garcia @Ubidots Developer
'''

import paho.mqtt.client as mqttClient
import time
import json
import random
import RPi.GPIO as GPIO
from gpiozero import Button

'''
global variables
'''
# Motor parameter
mode=GPIO.getmode()
Forward=23
Backward=24
sleeptime=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)

#Button parameter
button1 = Button(14, bounce_time=1)
button2 = Button(15, bounce_time=1)

# MQTT parameter
connected = False  # Stores the connection status
BROKER_ENDPOINT = "industrial.api.ubidots.com"
TLS_PORT = 1883  # MQTT port
MQTT_USERNAME = ""  # Put here your Ubidots TOKEN
MQTT_PASSWORD = ""  # Leave this in blank
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "(device label)/#" #Change this to your device label

'''
Functions to process incoming and outgoing streaming
'''
def forward(): #open curtain
    curtain_open = button1.is_pressed
    while not curtain_open:
        GPIO.output(Forward, GPIO.HIGH)
        curtain_open = button1.is_pressed
        #print(button1.is_pressed)
    print("Curtain Opened!")
    GPIO.output(Forward, GPIO.LOW)

def reverse(): #closed curtain
    curtain_closed = button2.is_pressed
    while not curtain_closed:
        GPIO.output(Backward, GPIO.HIGH)
        curtain_closed = button2.is_pressed
        #print(button2.is_pressed)
    print("Curtain Closed!")
    #print(button2.is_pressed)
    GPIO.output(Backward, GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    if rc == 0:
        print("[INFO] Connected to broker")
        connected = True  # Signal connection
    else:
        print("[INFO] Error, connection failed")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.connect(broker_endpoint, port=port)
        topic = "{}{}".format(TOPIC, DEVICE_LABEL)
        mqtt_client.subscribe(topic)
        mqtt_client.on_message = on_message
        mqtt_client.loop_forever()

        attempts = 0

        while not connected and attempts < 5:  # Wait for connection
            print(connected)
            print("Attempting to connect...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    return True

def on_message(client, userdata, message):
    if message.topic == "/v1.6/devices/mentor_ham/curtain-command/lv":
        print("incoming data: " ,str(message.payload.decode("utf-8")))
        command = str(message.payload.decode("utf-8"))
        if command == "1.0":
            print("closed curtain command received!")
            reverse()
        elif command == "0.0":
            print("open curtain command received!")
            forward()
           
if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    while True:
        connect(mqtt_client, MQTT_USERNAME,MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT)
