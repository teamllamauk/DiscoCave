#!/usr/bin/env python3

import RPi.GPIO as rGPIO

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

btn_red_pin = 25
btn_green_pin = 12
btn_blue_pin = 7
btn_orange_pin = 23
btn_white_pin = 6

led_red_pin = 8
led_green_pin = 5
led_blue_pin = 1
led_orange_pin = 24
led_white_pin = 13

global btn_red_flag
global btn_green_flag
global btn_blue_flag
global btn_orange_flag
global btn_white_flag

btn_red_flag = 0
btn_green_flag = 0
btn_blue_flag = 0
btn_orange_flag = 0
btn_white_flag = 0

rGPIO.setup(btn_red_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_green_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_blue_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_orange_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_white_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.setup(led_green_pin,rGPIO.OUT)
rGPIO.setup(led_blue_pin,rGPIO.OUT)
rGPIO.setup(led_orange_pin,rGPIO.OUT)
rGPIO.setup(led_white_pin,rGPIO.OUT)

rGPIO.output(led_red_pin,rGPIO.LOW)
rGPIO.output(led_green_pin,rGPIO.LOW)
rGPIO.output(led_blue_pin,rGPIO.LOW)
rGPIO.output(led_orange_pin,rGPIO.LOW)
rGPIO.output(led_white_pin,rGPIO.LOW)

def btn_Callback(button_pin):
    
    global btn_red_flag
    global btn_green_flag
    global btn_blue_flag
    global btn_orange_flag
    global btn_white_flag
    
    print (button_pin)
    if button_pin == btn_red_pin:
        if btn_red_flag == 0:
            rGPIO.output(led_red_pin,rGPIO.HIGH)
            btn_red_flag = 1
        else:
            rGPIO.output(led_red_pin,rGPIO.LOW)
            btn_red_flag = 0
    elif button_pin == btn_green_pin:
        if btn_green_flag == 0:
            rGPIO.output(led_green_pin,rGPIO.HIGH)
            btn_green_flag = 1
        else:
            rGPIO.output(led_green_pin,rGPIO.LOW)
            btn_green_flag = 0
    elif button_pin == btn_blue_pin:
        if btn_blue_flag == 0:
            rGPIO.output(led_blue_pin,rGPIO.HIGH)
            btn_blue_flag = 1
        else:
            rGPIO.output(led_blue_pin,rGPIO.LOW)
            btn_blue_flag = 0
    elif button_pin == btn_orange_pin:
        if btn_orange_flag == 0:
            rGPIO.output(led_orange_pin,rGPIO.HIGH)
            btn_orange_flag = 1
        else:
            rGPIO.output(led_orange_pin,rGPIO.LOW)
            btn_orange_flag = 0
    elif button_pin == btn_white_pin:
        if btn_white_flag == 0:
            rGPIO.output(led_white_pin,rGPIO.HIGH)
            btn_white_flag = 1
        else:
            rGPIO.output(led_white_pin,rGPIO.LOW)
            btn_white_flag = 0


rGPIO.add_event_detect(btn_red_pin, rGPIO.FALLING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_green_pin, rGPIO.FALLING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_blue_pin, rGPIO.FALLING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_orange_pin, rGPIO.FALLING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_white_pin, rGPIO.FALLING, callback=btn_Callback, bouncetime=500)

# Main loop
while True:
    a = 1
