# Halloween Pi
Collection of Raspberry Pi driven Halloween props

## MotionSkull

Uses a [PIR Motion detector](https://www.adafruit.com/product/189) as an activator. The HIGH signal triggers a custom breakout board of three [2N3904](https://www.sparkfun.com/datasheets/Components/2N3904.pdf) transistors that drive three [12v LEDs](https://www.amazon.com/gp/product/B07PVVL2S6) (for that extra bright punch)

Currently, there are modes for solid eyes, flashing synchronously, and flashing L/R alternately.

There is a basic time check to keep it off from 1am to 6pm using local system time. If not dark it will sleep for 30 minutes between checks. 
The polling loop is nothing fancy, just something to keep things from slamming the CPU and thus the battery.


