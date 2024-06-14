import RPi.GPIO as gpio
import time
import datetime

gpio.setmode(gpio.BCM)

# defini le port GPIO 4 comme etant une sortie output
gpio.setup(17, gpio.OUT)

# Mise a 1 pendant 2 secondes puis 0 pendant 2 seconde
while True:
    print("on")
    gpio.output(17, gpio.HIGH)
    time.sleep(2)
    print("off")
    gpio.output(17, gpio.LOW)
    time.sleep(2)

datetime.datetime.now()