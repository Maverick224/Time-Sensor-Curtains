# Here is the configuration:
# Connect your button NO pin to GPIO 14 & 15 (pin 8 & 10)
# Connect your button COM pin to GND

from gpiozero import Button
import time

button1 = Button(14, bounce_time=1)
button2 = Button(15, bounce_time=1)

while True: 
    if button1.is_pressed: 
        print("button1 pressed")
        time.sleep(1)
    if button2.is_pressed:
        print("button2 pressed")
        time.sleep(1)
    time.sleep(1)
