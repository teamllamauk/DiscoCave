#!/usr/bin/env python3

import time
import RPi.GPIO as rGPIO

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

led_red_pin = 8
led_green_pin = 5
led_blue_pin = 1
led_orange_pin = 24
led_white_pin = 13

rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.setup(led_green_pin,rGPIO.OUT)
rGPIO.setup(led_blue_pin,rGPIO.OUT)
rGPIO.setup(led_orange_pin,rGPIO.OUT)
rGPIO.setup(led_white_pin,rGPIO.OUT)

rGPIO.output(led_red_pin,rGPIO.LOW)
rGPIO.output(led_green_pin,rGPIO.LOW)
rGPIO.output(led_blue_pin,rGPIO.LOW)
rGPIO.output(led_orange_pin,rGPIO.High)
rGPIO.output(led_white_pin,rGPIO.LOW)

pwm1=GPIO.PWM(led_red_pin,1000)  # We need to activate PWM on LED1 so we can dim, use 1000 Hz 
pwm2=GPIO.PWM(led_green_pin,1000)
pwm3=GPIO.PWM(led_blue_pin,1000)
pwm4=GPIO.PWM(led_white_pin,1000)
pwm1.start(0)              # Start PWM at 0% duty cycle (off)             
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)
bright=1                   # Set initial brightness to 1%

while True:
    
