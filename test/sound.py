#!/usr/bin/env python3

#import os
import sys
import time
import threading
import pygame
import RPi.GPIO as rGPIO

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

led_red_pin = 8
rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.output(led_red_pin,rGPIO.LOW)

def playSound():
    print("Start")
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Development/DiscoCave/audio/vegimal.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        rGPIO.output(led_red_pin,rGPIO.HIGH)
        time.sleep(0.1)
        rGPIO.output(led_red_pin,rGPIO.Low)
        time.sleep(0.1)
    
    print("Finished")
    


try:
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/vegimal.mp3 &')
    #subprocess.Popen(['mpg123', '/home/pi/Development/DiscoCave/audio/vegimal.mp3'])
    #subprocess.call('mpg123 -q /home/pi/Development/DiscoCave/audio/veg.mp3 &')
    
    t1 = threading.Thread(target=playSound)
    t1.start()
    
    
    #pygame.mixer.init()
    #pygame.mixer.music.load("/home/pi/Development/DiscoCave/audio/vegimal.mp3")
    #pygame.mixer.music.play()
    #while pygame.mixer.music.get_busy() == True:
    #    print(".")
    
    #print("Finished")
    
except:
    print("Unexpected error:", sys.exc_info()[0])
