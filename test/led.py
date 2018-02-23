#!/usr/bin/env python3

import sys
import time

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

#strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rgb')
strip = apa102.APA102(num_led=60, global_brightness=5, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

def solidColour(ledColour):
    strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledColour) 
    strip.show()
   
    
solidColour(0xFF0000) #Red
time.sleep(2)
solidColour(0xFFA500) #Orange
time.sleep(2)
solidColour(0xFFFF00) #Yellow
time.sleep(2)
solidColour(0x00FF00) #Green
time.sleep(2)
solidColour(0x0000FF) #Blue
time.sleep(2)
solidColour(0x4B0082) #Indigo
time.sleep(2)
solidColour(0xEE82EE) #Violet
time.sleep(2)

strip.clear_strip()
strip.cleanup()
