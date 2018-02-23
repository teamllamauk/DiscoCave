#!/usr/bin/env python3

import sys
import time

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

# Prepare a few individual pixels
strip.set_pixel_rgb(12, 0xFF0000) # Red
strip.show()
time.sleep(5)
strip.clear_strip()

strip.set_pixel_rgb(12, 0x00FF00) # Green
strip.show()
time.sleep(5)
strip.clear_strip()

strip.set_pixel_rgb(12, 0x0000FF) # Blue
strip.show()
time.sleep(5)
strip.clear_strip()

strip.set_pixel_rgb(12, 0xFFFFFF) # White
strip.show()
time.sleep(5)
strip.clear_strip()

# Copy the buffer to the Strip (i.e. show the prepared pixels)


# Wait a few Seconds, to check the result


# Clear the strip and shut down

strip.cleanup()
