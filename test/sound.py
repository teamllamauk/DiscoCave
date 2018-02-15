#!/usr/bin/env python3

#import os
import sys
import time
import threading
import RPi.GPIO as GPIO

from pygame import mixer


def playSound():
    print("Start Playback")
    mixer.init()
    mixer.music.load('/home/pi/Development/DiscoCave/audio/vegimal.mp3')
    mixer.music.play()
    print("End Playback")


try:
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/vegimal.mp3 &')
    #subprocess.Popen(['mpg123', '/home/pi/Development/DiscoCave/audio/vegimal.mp3'])
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/veg.mp3 &')
    
    t1 = threading.Thread(target=playSound)
    t1.start()
            
    while mixer.get_busy():
        print(".")
    
    print("Finished")
    
except:
    print("Unexpected error:", sys.exc_info()[0])
