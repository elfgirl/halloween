#!/usr/bin/env python3

import datetime
import time

import RPi.GPIO as GPIO

timezone_offset = -8.0  # Pacific Standard Time (UTC−08:00)
tzinfo = datetime.timezone(datetime.timedelta(hours=timezone_offset))
time_allowed_start = 17  # 6 PM
time_allowed_stop = 3

l_led_pin = 13  # define led_pin
r_led_pin = 19
a_led_pin = 26

lg_led_pin = 5  # define led_pin
rg_led_pin = 6

sensor_pin = 18


def setup():
    print('Setup')
    GPIO.setmode(GPIO.BCM)  # use PHYSICAL GPIO Numbering
    GPIO.setup(l_led_pin, GPIO.OUT)  # set the led_pin to OUTPUT mode
    GPIO.output(l_led_pin, GPIO.LOW)  # make led_pin output LOW level
    GPIO.setup(r_led_pin, GPIO.OUT)  # set the led_pin to OUTPUT mode
    GPIO.output(r_led_pin, GPIO.LOW)  # make led_pin output LOW level
    GPIO.setup(a_led_pin, GPIO.OUT)  # set the led_pin to OUTPUT mode
    GPIO.output(a_led_pin, GPIO.LOW)  # make led_pin output LOW level
    GPIO.setup(sensor_pin, GPIO.IN)  # set sensorPin to INPUT mode

    GPIO.setup(lg_led_pin, GPIO.OUT)  # set the led_pin to OUTPUT mode
    GPIO.output(lg_led_pin, GPIO.LOW)  # make led_pin output LOW level

    GPIO.setup(rg_led_pin, GPIO.OUT)  # set the led_pin to OUTPUT mode
    GPIO.output(rg_led_pin, GPIO.LOW)  # make led_pin output LOW level


def flash_eyes_sync():
    print('Flash  Sync Eyes start')
    GPIO.output(a_led_pin, GPIO.HIGH)
    for iteration in range(1, 5):
        GPIO.output(l_led_pin, GPIO.HIGH)
        GPIO.output(r_led_pin, GPIO.HIGH)

        # print('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_led_pin, GPIO.LOW)
        GPIO.output(r_led_pin, GPIO.LOW)

        # print('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_led_pin, GPIO.LOW)


def flash_eyes_alt():
    print('Flash Alt Eyes start')
    GPIO.output(a_led_pin, GPIO.HIGH)
    for iteration in range(1, 5):
        GPIO.output(l_led_pin, GPIO.HIGH)
        GPIO.output(r_led_pin, GPIO.LOW)

        # print('led turned on >>>')
        time.sleep(.3)
        GPIO.output(l_led_pin, GPIO.LOW)
        GPIO.output(r_led_pin, GPIO.HIGH)

        # print('led turned off <<<')
        time.sleep(.3)
    GPIO.output(a_led_pin, GPIO.LOW)


def solid_eyes_sync():
    turn_on_all_led()
    time.sleep(5)
    turn_off_leds()


def wait_for_dark():
    current_time = datetime.datetime.now(tzinfo)
    if time_allowed_stop < current_time.hour < time_allowed_start:
        print(f'Not Spooky Time {current_time.hour}')
        return True
    print(f'Spooky Time!!! {current_time.hour}')
    return False


def turn_off_leds():
    # print('Turn off all LEDs')
    GPIO.output(l_led_pin, GPIO.LOW)  # make led_pin output HIGH level to turn on led
    GPIO.output(r_led_pin, GPIO.LOW)  # make led_pin output HIGH level to turn on led
    GPIO.output(a_led_pin, GPIO.LOW)  # make led_pin output HIGH level to turn on led

    GPIO.output(rg_led_pin, GPIO.LOW)  # make led_pin output HIGH level to turn on led
    GPIO.output(lg_led_pin, GPIO.LOW)  # make led_pin output HIGH level to turn on led


def turn_on_all_led():
    GPIO.output(l_led_pin, GPIO.HIGH)  # make led_pin output HIGH level to turn on led
    GPIO.output(r_led_pin, GPIO.HIGH)  # make led_pin output HIGH level to turn on led
    GPIO.output(a_led_pin, GPIO.HIGH)  # make led_pin output HIGH level to turn on led

    GPIO.output(rg_led_pin, GPIO.HIGH)  # make led_pin output HIGH level to turn on led
    GPIO.output(lg_led_pin, GPIO.HIGH)  # make led_pin output HIGH level to turn on led


def loop():
    while True:

        if wait_for_dark():
            print('Not dark enough yet')
            time.sleep(60 * 30)  # Sleep for 30 minutes
            continue

        # Check Motion Sensor
        if GPIO.input(sensor_pin) == GPIO.HIGH:
            print("We've got a live one!")
            solid_eyes_sync()
            continue  # If we're active, skip right to next check and avoid polling sleep below
        else:
            turn_off_leds()

        time.sleep(.25)


def destroy():
    GPIO.cleanup()  # Release all GPIO
    print('Program is ending ... \n')


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
