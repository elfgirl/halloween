# SPDX-FileCopyrightText: 2017 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT

#
# Kaleidoscope_Eyes_NeoPixel_LED_Goggles.py
#
import time

import board
import neopixel

try:
    import urandom as random  # for v1.0 API support
except ImportError:
    import random

numpix = 32  # Number of NeoPixels
pixpin = board.D0  # Pin where NeoPixels are connected

mode = 0  # Current animation effect
offset = 0  # Position of spinny eyes

RED = [255,0,0]
ORANGE = [255,165,0]
YELLOW = [255,255,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
PURPLE = [153,0,153]
WHITE = [255,255,255]
PINK = [255,51,153]
BLACK = [0,0,0]

rgb_colors = (RED,ORANGE,YELLOW,GREEN,BLUE,PURPLE,BLACK,BLUE,PINK,WHITE,PINK,BLUE,BLACK)


MAX_SPARKS = 4

rgb_idx = 0  # index counter - primary color we are on
color = rgb_colors[rgb_idx]

#pixels = [BLACK] * numpix

prevtime = 0

pixels = neopixel.NeoPixel(pixpin, numpix, brightness=.7, auto_write=False)

prevtime = time.monotonic()

def decrement_step(value,increment):
    new_values = [0]*len(value)
    for x in range(0, len(value)):
        new_values[x] = value[x] - increment[x]
        if(value[x] < 0) :
            new_values[x] = 0
        if(value[x] > 255) :
            new_values[x] = 255
    return [int(new_values[0]),int(new_values[1]),int(new_values[2])]

FADE_TAIL = 4
FADE_STEPS = 4 # 1/4 every fade tail

while True:

    i = 0
    t = 0
    fade_index = 1

    # Random sparks - just one LED on at a time!
    if mode == 0:
        sparks = random.randint(0, MAX_SPARKS)
        for spark_count in range(0,sparks):
            i = random.randint(0, (numpix - 1))
            pixels[i] = color

        pixels.write()

        time.sleep(0.01)
        for clear_index in range(0, numpix):
            pixels[clear_index] = (0, 0, 0)

    # Spinny wheels (8 LEDs on at a time)
    elif mode == 1:

        fade_index = 0
        for pixel_index in range(0, numpix):
            # 4 pixels on...
            if ((offset + pixel_index) & 7) < FADE_TAIL:
                c = color
                if fade_index < FADE_TAIL:
                    for x in range(0, fade_index):
                        c = decrement_step(c, color_decrement)
                    fade_index = fade_index + 1
            else:
                fade_index = 0
                c = 0
            # print(c)
            pixels[pixel_index] = c  # First eye
            pixels[(numpix - 1) - pixel_index] = c  # Second eye (flipped)

        pixels.write()
        offset += 1
        time.sleep(0.05)

    t = time.monotonic()

    if (t - prevtime) > 15:  # Every 8 seconds...
        mode += 1  # Next mode
        if mode > 1:  # End of modes?
            mode = 0  # Start modes over

        if rgb_idx > len(rgb_colors) -1 :  # reset R-->G-->B rotation
            rgb_idx = 0

        color = rgb_colors[rgb_idx]  # next color assignment
        print(color)
        color_decrement = (int(color[0] / FADE_STEPS), int(color[1] / FADE_STEPS), int(color[2] / FADE_STEPS))
        rgb_idx += 1

        for i in range(0, numpix):
            pixels[i] = (0, 0, 0)

        prevtime = t
