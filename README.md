# Halloween Pi
Collection of Raspberry Pi driven Halloween props

## Cauldron

![GreenCauldron](images/Cauldron.jpg)

Uses a [Ultrasonice Distance Sensor](https://www.adafruit.com/product/4007) to activate a flexible [RBG LED strip](https://www.adafruit.com/product/4245) glued into the rim. The distance sensor acts as a beam break and flips the strip to blood red. It also sends a REST call to the sound server to trigger a spooky effect behind the candy taker

The sensor is a bit iffy in terms of reading, with occasional spikes and low points. To prevent unwanted triggers, there is a threshold for how many out of normal readings to trigger the effect (currently 2)

The RGB strip is independently powered by a bank of 8AAs, modulated by three [2N3904](https://www.sparkfun.com/datasheets/Components/2N3904.pdf) transistors

## MotionSkull

![Close Up of Skull](images/CloseUpSkull.jpeg)

Uses a [PIR Motion detector](https://www.adafruit.com/product/189) as an activator. The HIGH signal triggers a custom breakout board of three [2N3904](https://www.sparkfun.com/datasheets/Components/2N3904.pdf) transistors that drive three [12v LEDs](https://www.amazon.com/gp/product/B07PVVL2S6) (for that extra bright punch)

Currently, there are modes for solid eyes, flashing synchronously, and flashing L/R alternately.

There is a basic time check to keep it off from 1am to 6pm using UTC time and cheap datezone hack. See the Waterbug project for intelligent sunrise/sunset timers. If not dark it will sleep for 30 minutes between checks. 

The polling loop is nothing fancy, just something to keep things from slamming the CPU and thus the battery.

Added a supervisor configuration file to maintain execution. 

![ExtraBrightSkull](images/MotionSkull.jpg)

## BreatheSkull

Simple PMW based LED fade/pulse for the red eyes. The green stays an ambient green glow.  Set at the _bare_ minimum before flickering on the dim settings but does not turn off for a good pulsating effect

## Ambient SoundFX

Using the [Adafruit Speaker Bonnet](https://www.adafruit.com/product/3346) with these [install instructions](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi)
(https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage)

This provides a super simple REST based server to do either specific sounds or a random selection from all available. Great for hiding in trees and triggering via another Pi's sensor.
PyGame seems to the _easiest_ way to do sound on python linux, however does seem wrong

One thing to note is that music has to be mp3. Sounds have to wav. Multiple sounds can overap with repeated triggers, only one music file will play

* /sound
* /sound/<string:sound_file_name>
* /music
* /music/<string:music_file_name>

The file names are not raw names. Instead, they are a table lookup to keep some semblance of raw user input sanity

