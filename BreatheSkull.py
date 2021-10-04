#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO

l_ledPin = 13  # define ledPin
r_ledPin = 19
a_ledPin = 26
sensorPin = 18


def setup():
    global p_l
    global p_r

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(l_ledPin, GPIO.OUT)
    GPIO.output(l_ledPin, GPIO.LOW)

    GPIO.setup(r_ledPin, GPIO.OUT)
    GPIO.output(r_ledPin, GPIO.LOW)

    GPIO.setup(a_ledPin, GPIO.OUT)
    GPIO.output(a_ledPin, GPIO.HIGH)  # Keep that green glow

    p_l = GPIO.PWM(l_ledPin, 500)  # set PWM Frequence to 500Hz
    p_l.start(0)  # set initial Duty Cycle to 0

    p_r = GPIO.PWM(r_ledPin, 250)  # set PWM Frequence to 500Hz
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
