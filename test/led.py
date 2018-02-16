#!/usr/bin/env python3

import sys
import time

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rbg')

strip.clear_strip()

# Prepare a few individual pixels
strip.set_pixel_rgb(12, 0xFF0000) # Red
strip.set_pixel_rgb(24, 0xFFFFFF) # White
strip.set_pixel_rgb(36, 0x00FF00) # Green
strip.set_pixel_rgb(48, 0x0000FF) # Green

# Copy the buffer to the Strip (i.e. show the prepared pixels)
strip.show()

# Wait a few Seconds, to check the result
time.sleep(20)

# Clear the strip and shut down
strip.clear_strip()
strip.cleanup()
