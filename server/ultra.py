#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic

# TODO add a filter - this sensor is realy shitty

import RPi.GPIO as GPIO
import time

Tr = 23
Ec = 24

def checkdist():       #Reading distance
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    while not GPIO.input(Ec):
        pass
    t1 = time.time()
    while GPIO.input(Ec):
        pass
    t2 = time.time()
    return round((t2-t1)*340/2,2)

if __name__ == '__main__':
    try:
        while True:
            dist = round(checkdist(),2)
            print(dist)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
