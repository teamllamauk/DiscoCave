#!/usr/bin/env python3

#import os
import sys
import time
import threading
import pygame
import RPi.GPIO as rGPIO

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

led_orange_pin = 24
rGPIO.setup(led_orange_pin,rGPIO.OUT)
rGPIO.output(led_orange_pin,rGPIO.LOW)

def playSound():
    print("Start")
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/Development/DiscoCave/audio/vegimal.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        rGPIO.output(led_orange_pin,rGPIO.HIGH)
        time.sleep(0.25)
        rGPIO.output(led_orange_pin,rGPIO.LOW)
        time.sleep(0.25)
    
    rGPIO.output(led_orange_pin,rGPIO.LOW)
    print("Finished")    


try:        
    t1 = threading.Thread(target=playSound)
    t1.start()    
    
except:
    print("Unexpected error:", sys.exc_info()[0])
