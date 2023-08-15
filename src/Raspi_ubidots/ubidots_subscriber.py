'''
Sends data to Ubidots using MQTT
Example provided by Jose Garcia @Ubidots Developer
'''

import paho.mqtt.client as mqttClient
import time
import json
import random

'''
global variables
'''
connected = False  # Stores the connection status
BROKER_ENDPOINT = "industrial.api.ubidots.com"
TLS_PORT = 1883  # MQTT port
MQTT_USERNAME ="BBFF-sn8vaxyj3ANr6f5nk2C8gKRONPhZA9"  # Put here your Ubidots TOKEN
MQTT_PASSWORD = ""  # Leave this in blank
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "mvr/#" #Change this to your device label

'''
Functions to process incoming and outgoing streaming
'''

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
    # print("incoming data: " ,str(message.payload.decode("utf-8")))

     if message.topic == "/v1.6/devices/mvr/control_motor/lv":
         # print("control command: " ,str(message.payload.decode("utf-8")))
         # do something according to the command
         motor_command = str(message.payload.decode("utf-8"))
         if motor_command == "1.0": #motor  dinyalakan
             print("motor dinyalakan")
         else:
             print("motor dimatikan")
     #elif message.topic == "/v1.6/devices/mvr/lampu_1":
      #   print("Lamp State: " ,str(message.payload.decode("utf-8")))

if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    while True:
        connect(mqtt_client, MQTT_USERNAME,MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT)
