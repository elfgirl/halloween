#!/usr/bin/env python3
import time

import RPi.GPIO as GPIO
from requests import request

blue_ledPin = 16  # define ledPin
red_ledPin = 20
green_ledPin = 21

rgb_pins = [red_ledPin, green_ledPin, blue_ledPin]

trigger_pin = 23
echo_pin = 24
MAX_DISTANCE = 220  # define the maximum measuring distance, unit: cm
max_time_out = MAX_DISTANCE * 60  # calculate timeout according to the maximum measuring distance


def pulse_in(pin, level, time_out):  # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while GPIO.input(pin) != level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    t0 = time.time()
    while GPIO.input(pin) == level:
        if (time.time() - t0) > time_out * 0.000001:
            return 0
    pulse_time = (time.time() - t0) * 1000000
    return pulse_time


def get_sonar():  # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigger_pin, GPIO.HIGH)  # make trigPin output 10us HIGH level
    time.sleep(0.00001)  # 10us
    GPIO.output(trigger_pin, GPIO.LOW)  # make trigPin output LOW level
    ping_time = pulse_in(echo_pin, GPIO.HIGH, max_time_out)  # read plus time of echoPin
    distance = ping_time * 340.0 / 2.0 / 10000.0  # calculate distance with sound speed 340m/s
    return distance


def setup():
    GPIO.setmode(GPIO.BCM)  # use PHYSICAL GPIO Numbering
    GPIO.setup(trigger_pin, GPIO.OUT)  # set trigPin to OUTPUT mode
    GPIO.setup(echo_pin, GPIO.IN)  # set echoPin to INPUT mode

    GPIO.setup(green_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(green_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(red_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(red_ledPin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.setup(blue_ledPin, GPIO.OUT)  # set the ledPin to OUTPUT mode
    GPIO.output(blue_ledPin, GPIO.LOW)  # make ledPin output LOW level


def led_on(on_pin):
    for off_pin in rgb_pins:
        GPIO.output(off_pin, GPIO.LOW)  # make ledPin output LOW level
    GPIO.output(on_pin, GPIO.HIGH)  # make ledPin output LOW level


def loop():
    color_flipped = False
    out_of_range_count = 0

    while True:
        distance = get_sonar()  # get distance

        print("The distance is : %.2f cm" % distance)
        if distance > 28.0 or distance < 20.0:
            print('Priming')
            out_of_range_count = out_of_range_count + 1
        else:
            out_of_range_count = 0
            led_on(green_ledPin)
            color_flipped = False

        if out_of_range_count > 1:  # Two anomalies
            if not color_flipped:
                led_on(red_ledPin)
                color_flipped = True
                request('GET', 'http://moonberry.local:5001/sound')
                print("Aaaaahhhhhoooo")

        time.sleep(.05)


if __name__ == '__main__':  # Program entrance
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()  # release GPIO resource
