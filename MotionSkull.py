#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import datetime

l_ledPin = 13    # define ledPin
r_ledPin = 19
a_ledPin = 26
sensorPin = 18

def setup():
    GPIO.setmode(GPIO.BCM)       # use PHYSICAL GPIO Numbering
    GPIO.setup(l_ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(l_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(r_ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(r_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(a_ledPin, GPIO.OUT)   # set the ledPin to OUTPUT mode
    GPIO.output(a_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode

def flash_eyes_sync() :
    GPIO.output(a_ledPin, GPIO.HIGH)
    for iteration in range(1,5) :
        GPIO.output(l_ledPin, GPIO.HIGH)
        GPIO.output(r_ledPin, GPIO.HIGH)

        print ('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_ledPin, GPIO.LOW)
        GPIO.output(r_ledPin, GPIO.LOW)

        print ('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_ledPin, GPIO.LOW)

def flash_eyes_alt() :
    GPIO.output(a_ledPin, GPIO.HIGH)
    for iteration in range(1,5) :
        GPIO.output(l_ledPin, GPIO.HIGH)
        GPIO.output(r_ledPin, GPIO.LOW)

        print ('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_ledPin, GPIO.LOW)
        GPIO.output(r_ledPin, GPIO.HIGH)

        print ('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_ledPin, GPIO.LOW)

def solid_eyes_sync() :
    GPIO.output(l_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
    GPIO.output(r_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
    GPIO.output(a_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led

    time.sleep(1.5)

    GPIO.output(l_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(r_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(a_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led

def wait_for_dark():
    current_time = datetime.datetime.now()
    if current_time.hour > 0 and current_time.hour < 18 :
        return True
    return False

def turn_off_leds():
    GPIO.output(l_ledPin,GPIO.LOW) # turn off led
    GPIO.output(l_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(r_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(a_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led

def loop():
    while True:

        if wait_for_dark() :
            time.sleep(60*30) # Sleep for 30 minutes
            continue

        # Check Motion Sensor
        if GPIO.input(sensorPin)==GPIO.HIGH:
            solid_eyes_sync()
        else :
            turn_off_leds()

        time.sleep(.25)

def destroy():
    GPIO.cleanup()                      # Release all GPIO

if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()

