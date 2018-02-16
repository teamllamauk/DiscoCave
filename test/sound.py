#!/usr/bin/env python3

#import os
import sys
import time
import threading
import pygame
import RPi.GPIO as rGPIO
from random import randint

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

btn_orange_pin = 23
led_orange_pin = 24

rGPIO.setup(btn_orange_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

rGPIO.setup(led_orange_pin,rGPIO.OUT)
rGPIO.output(led_orange_pin,rGPIO.LOW)

global btn_orange_flag
btn_orange_flag = 0

def btn_Callback(button_pin):
    global btn_orange_flag
    
    if button_pin == btn_orange_pin:
        if btn_orange_flag == 0 :
            t1 = threading.Thread(target=playSound)
            t1.start() 
    

rGPIO.add_event_detect(btn_orange_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)

def playSound():
    global btn_orange_flag
    btn_orange_flag = 1
    
    audio_rand = randint(1, 25)    # Pick a random number between 1 and 25.
    
    if audio_rand == 25 :
        sound_file = "/home/pi/Development/DiscoCave/audio/vegimal.mp3"
    else :
        sound_file = "/home/pi/Development/DiscoCave/audio/octoalert.mp3"
    
    print("Start")
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        rGPIO.output(led_orange_pin,rGPIO.HIGH)
        time.sleep(0.25)
        rGPIO.output(led_orange_pin,rGPIO.LOW)
        time.sleep(0.25)
    
    rGPIO.output(led_orange_pin,rGPIO.LOW)
    print("Finished")
    btn_orange_flag = 0


# Main loop
while True:
    a = 1
    
#try:        
#    t1 = threading.Thread(target=playSound)
#    t1.start()    
    
#except:
#    print("Unexpected error:", sys.exc_info()[0])
