#!/usr/bin/env python3

#import os
import sys
import time
import threading
import RPi.GPIO as GPIO
import pygame


#def playSound():
    #pygame.mixer.init()
    #pygame.mixer.music.load("/home/pi/Development/DiscoCave/audio/vegimal.mp3")
    #pygame.mixer.music.play()
    


try:
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/vegimal.mp3 &')
    #subprocess.Popen(['mpg123', '/home/pi/Development/DiscoCave/audio/vegimal.mp3'])
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/veg.mp3 &')
    
    #t1 = threading.Thread(target=playSound)
    #t1.start()
    
    
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Development/DiscoCave/audio/vegimal.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        print(".")
    
    print("Finished")
    
except:
    print("Unexpected error:", sys.exc_info()[0])
