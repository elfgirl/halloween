#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

l_led_pin = 13  # define led_pin
r_led_pin = 19
a_led_pin = 26
sensorPin = 18


def setup():
    global p_l
    global p_r

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(l_led_pin, GPIO.OUT)
    GPIO.output(l_led_pin, GPIO.LOW)

    GPIO.setup(r_led_pin, GPIO.OUT)
    GPIO.output(r_led_pin, GPIO.LOW)

    GPIO.setup(a_led_pin, GPIO.OUT)
    GPIO.output(a_led_pin, GPIO.HIGH)  # Keep that green glow

    p_l = GPIO.PWM(l_led_pin, 500)  # set PWM Frequence to 500Hz
    p_l.start(0)  # set initial Duty Cycle to 0

    p_r = GPIO.PWM(r_led_pin, 250)  # set PWM Frequence to 500Hz
    p_r.start(0)  # set initial Duty Cycle to 0


def loop():
    while True:
        for dc in range(10, 101, 1):  # make the led brighter
            p_l.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            p_r.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            time.sleep(0.05)
        time.sleep(2)
        for dc in range(100, 10, -1):  # make the led darker
            p_l.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            p_r.ChangeDutyCycle(dc)  # set dc value as the duty cycle
            time.sleep(0.05)
        time.sleep(2)


def destroy():
    p_l.stop()  # stop PWM
    p_r.stop()  # stop PWM
    GPIO.cleanup()  # Release all GPIO


if __name__ == '__main__':  # Program entrance
    print('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
