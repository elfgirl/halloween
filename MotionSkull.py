#!/usr/bin/env python3

import datetime
import random
import time

import RPi.GPIO as GPIO

timezone_offset = -8.0  # Pacific Standard Time (UTC−08:00)
tzinfo = datetime.timezone(datetime.timedelta(hours=timezone_offset))
time_allowed_start = 18  # 6 PM
time_allowed_stop = 2

l_ledPin = 13  # define ledPin
r_ledPin = 19
a_ledPin = 26
sensorPin = 18


def setup():
    print('Setup')
    GPIO.setmode(GPIO.BCM)  # use PHYSICAL GPIO Numbering
    GPIO.setup(l_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(l_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(r_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(r_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(a_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(a_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode


def flash_eyes_sync():
    print('Flash  Sync Eyes start')
    GPIO.output(a_ledPin, GPIO.HIGH)
    for iteration in range(1, 5):
        GPIO.output(l_ledPin, GPIO.HIGH)
        GPIO.output(r_ledPin, GPIO.HIGH)

        #print('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_ledPin, GPIO.LOW)
        GPIO.output(r_ledPin, GPIO.LOW)

        #print('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_ledPin, GPIO.LOW)


def flash_eyes_alt():
    print('Flash Alt Eyes start')
    GPIO.output(a_ledPin, GPIO.HIGH)
    for iteration in range(1, 5):
        GPIO.output(l_ledPin, GPIO.HIGH)
        GPIO.output(r_ledPin, GPIO.LOW)

        #print('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_ledPin, GPIO.LOW)
        GPIO.output(r_ledPin, GPIO.HIGH)

        #print('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_ledPin, GPIO.LOW)


def solid_eyes_sync():
    turn_on_leds()
    time.sleep(5)
    turn_off_leds()


def wait_for_dark():
    current_time = datetime.datetime.now(tzinfo)
    if current_time.hour > time_allowed_stop and current_time.hour < time_allowed_start:
        print(f'Not Spooky Time {current_time.hour}')
        return True
    #print(f'Spooky Time!!! {current_time.hour}')
    return False


def turn_off_leds():
    #print('Turn off all LEDs')
    GPIO.output(l_ledPin, GPIO.LOW)  # turn off led
    GPIO.output(l_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(r_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led
    GPIO.output(a_ledPin, GPIO.LOW)  # make ledPin output HIGH level to turn on led


def turn_on_leds():
    #print('Turn on all LEDs')
    GPIO.output(l_ledPin, GPIO.HIGH)  # turn off led
    GPIO.output(l_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
    GPIO.output(r_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led
    GPIO.output(a_ledPin, GPIO.HIGH)  # make ledPin output HIGH level to turn on led


def loop():
    while True:

        if wait_for_dark():
            print('Not dark enough yet')
            time.sleep(60 * 30)  # Sleep for 30 minutes
            continue

        # Check Motion Sensor
        if GPIO.input(sensorPin) == GPIO.HIGH:
            print("We've got a live one!")
            solid_eyes_sync()
            continue # If we're active, skip right to next check and avoid polling sleep below
        else:
            turn_off_leds()

        time.sleep(.25)


def destroy():
    GPIO.cleanup()  # Release all GPIO
    print('Program is endinng ... \n')


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
