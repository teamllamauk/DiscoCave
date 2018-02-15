#!/usr/bin/env python3

import os
import sys

try:
    #os.system('mpg123 -q /home/pi/Development/DiscoCave/audio/vegimal.mp3 &')
    subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/veg.mp3 &')
except:
    print("Error")
