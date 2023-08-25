'''
Sends data to Ubidots using MQTT
Example provided by Jose Garcia @Ubidots Developer, modified a little bit by HAM
'''

import paho.mqtt.client as mqttClient
import time
import json
import random
import Adafruit_DHT
from gpiozero import Button

'''
global variables
'''
connected = False  # Stores the connection status
BROKER_ENDPOINT = "industrial.api.ubidots.com"
TLS_PORT = 1883  # MQTT port
MQTT_USERNAME = ""  # Put here your Ubidots TOKEN
MQTT_PASSWORD = ""  # Leave this in blank
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "" #Change this to your device label

#Parameter DHT 11
sensor = Adafruit_DHT.DHT11
pin = 4

#Parameter limit switch
button1 = Button(14, bounce_time=1) #curtain open
button2 = Button(15, bounce_time=1) #curtain closed
curtain_status = 0 #ny default, curtain is assumed open

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


def on_publish(client, userdata, result):
    print("Published!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

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


def publish(mqtt_client, topic, payload):

    try:
        mqtt_client.publish(topic, payload)

    except Exception as e:
        print("[ERROR] Could not publish data, error: {}".format(e))


def main(mqtt_client):
    global curtain_status
    #read Temperature and Humidity Data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    #curtain status: 0 for open, 1 for closed
    if button1.is_pressed:
        curtain_status = 0
    if button2.is_pressed:
        curtain_status = 1    
    
    payload = json.dumps({"temperature": temperature,"humidity": humidity,\
                          "curtain-status": curtain_status})
    
    # publish two example
    # humidity = int(random.random()*100)
    # payload = json.dumps({"temperature": val, "humidity": humidity})
    
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)
    if not connect(mqtt_client, MQTT_USERNAME,
                   MQTT_PASSWORD, BROKER_ENDPOINT, TLS_PORT):
        return False

    publish(mqtt_client, topic, payload)

    return True


if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    while True:
        main(mqtt_client)
        time.sleep(10)
