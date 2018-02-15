#!/usr/bin/env python3

#import os
import sys
from pygame import mixer

try:
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/vegimal.mp3 &')
    #subprocess.Popen(['mpg123', '/home/pi/Development/DiscoCave/audio/vegimal.mp3'])
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/veg.mp3 &')
    
    mixer.init()
    mixer.music.load('/home/pi/Development/DiscoCave/audio/vegimal.mp3')
    mixer.music.play()
    
    while mixer.get_busy():
        print(".")
    
    print("Finished")
    
except:
    print("Unexpected error:", sys.exc_info()[0])
