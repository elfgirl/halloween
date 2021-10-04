# Halloween Pi
Collection of Raspberry Pi driven Halloween props

## MotionSkull

Uses a [PIR Motion detector](https://www.adafruit.com/product/189) as an activator. The HIGH signal triggers a custom breakout board of three [2N3904](https://www.sparkfun.com/datasheets/Components/2N3904.pdf) transistors that drive three [12v LEDs](https://www.amazon.com/gp/product/B07PVVL2S6) (for that extra bright punch)

Currently, there are modes for solid eyes, flashing synchronously, and flashing L/R alternately.

There is a basic time check to keep it off from 1am to 6pm using UTC time and cheap datezone hack. See the Waterbug project for intelligent sunrise/sunset timers. If not dark it will sleep for 30 minutes between checks. 

The polling loop is nothing fancy, just something to keep things from slamming the CPU and thus the battery.

Added a supervisor configuration file to maintain execution. 

## BreatheSkull

Simple PMW based LED fade/pulse for the red eyes. The green stays an ambient green glow.  Set at the _bare_ minimum before flickering on the dim settings but does not turn off for a good pulsating effect
