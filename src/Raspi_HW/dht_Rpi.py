# Connect the DHT11 sensor and configure your Rpi by following on this link
# https://iotstarters.com/connecting-dht11-sensor-with-raspberry-pi-3-4-using-python/

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 4
while True:
     humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
     print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))