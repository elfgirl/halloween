#from adafruit_circuitplayground import cp
import time
import board
from rainbowio import colorwheel
import neopixel
from digitalio import DigitalInOut, Direction
from time import sleep

try:
  import ulab.numpy as np
except ImportError:
  import numpy as np


RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (153,0,153)
WHITE = (255,255,255)
PINK = (255,51,153)
BLACK = (0,0,0)

print("Starting up")

print('Das Blinking Lights')

def decrement_step(value,increment):
    new_values = [0]*len(value)
    for x in range(0, len(value)):
        new_values[x] = value[x] - increment[x]
        if(value[x] < 0) :
            new_values[x] = 0
        if(value[x] > 255) :
            new_values[x] = 255
    return (int(new_values[0]),int(new_values[1]),int(new_values[2]))

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.2, auto_write=False)

NUM_LEDS = 10
COLOR = PURPLE
TRAIL_LENGTH = 3
DECREMENT = ( int(COLOR[0] / TRAIL_LENGTH), int(COLOR[1] / TRAIL_LENGTH), int(COLOR[2] / TRAIL_LENGTH))

pulse = [BLACK] * 10

print('Init Array')
pulse[0] = COLOR

def pulse(array, start_index, direction) :
    if direction > 0 :
        start_range = start_index
        end_range = start_index + TRAIL_LENGTH
    else:
        start_range = start_index
        end_range = start_index - TRAIL_LENGTH

    for length_index in range(start_range, end_range) :
        pulse[start_index] = COLOR
        for call_index in range(start_index, end_range) :
            decrement = COLOR
            for step_index in range(1, TRAIL_LENGTH):
                decrement = decrement_step(decrement, DECREMENT)

            # for y in range(1, TAIL_LENGTH):
            #     new_list[y - 1] = (0, 0, int(255 - (DEC * y)))
            #
print(pulse)

shifted_arr = np.array(pulse)

cur_index = -1
while True :
    shifted_arr = np.roll(shifted_arr, -1, axis=0)
    shifted_list = shifted_arr.tolist()
    print(shifted_list)
    for x in range(0, 10) :
        pixels[x] = shifted_list[x]
    pixels.show()
    sleep(.1)


