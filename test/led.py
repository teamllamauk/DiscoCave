#!/usr/bin/env python3

# Imports
import sys
import time
import threading
import colorsys
import RPi.GPIO as rGPIO

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rgb')
#strip = apa102.APA102(num_led=60, global_brightness=5, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

global availableColours
global selectedColourPos
global killThread
killThread = False

availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
selectedColourPos = 0

led_red_pin = 8
led_green_pin = 5
led_blue_pin = 1
led_orange_pin = 24
led_white_pin = 13

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

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

def endThread():
    global killThread
    killThread = True
    print("Kill Thread")

def convertHSVtoRGB(hsvColour):
    rgbColour = colorsys.hsv_to_rgb(hsvColour/360,1,1)
    #print("HSV: ", hsvColour)
        
    hR = int(rgbColour[0] * 256)
    if hR == 256: hR = 255    
        
    hG = int(rgbColour[1] * 256)
    if hG == 256: hG = 255
    
    hB = int(rgbColour[2] * 256)
    if hB == 256: hB = 255
    
    rgbIntColour = (hR, hG, hB)    
    rgbHexColour = '0x%02x%02x%02x' % rgbIntColour
    
    #print(rgbHexColour)
    return int(rgbHexColour, 16)


def buttonColour():
    global availableColours
    global selectedColourPos
    
    selectedColourPos = selectedColourPos + 1
    if selectedColourPos > 11: selectedColourPos = 0
        
    ledHSVColour = availableColours[selectedColourPos]
    solidColour(ledHSVColour)


def solidColour(ledHSVColour):
    print("Solid Colour")        
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    
    #strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledRGBColour)        
    strip.show()


def rainbow(delay):
    global availableColours
    global selectedColourPos
    global killThread
    
    killThread = True
    
    while killThread == False:
        Print("Rainbow")
        solidColour(availableColours[selectedColourPos])
        selectedColourPos = selectedColourPos + 1
        if selectedColourPos > 11: selectedColourPos = 0
        time.sleep(delay)


def rotateLEDs(delay):
    global availableColours
    global selectedColourPos    
    global killThread
    
    killThread = True
    
    while killThread == False:
        print("Rotate")
        for x in range(0, 60):
            ledOne = x
            ledTwo = x + 1
            ledThree = x + 2            
            
            ledHSVColour = availableColours[selectedColourPos]    
            ledRGBColour = convertHSVtoRGB(ledHSVColour)
            
            strip.clear_strip()
            strip.set_pixel_rgb(ledOne, ledRGBColour, 5)
            if ledTwo < 61: strip.set_pixel_rgb(ledTwo, ledRGBColour)
            if ledThree < 61: strip.set_pixel_rgb(ledThree, ledRGBColour, 5)
            strip.show()
            time.sleep(delay)


def bounceLEDs(delay):    
    global availableColours
    global selectedColourPos
    global killThread
    
    killThread = True
    
    while killThread == False:
        print("Bounce")
        for x in range(0, 60):
            ledOne = x
            ledTwo = x + 1
            ledThree = x + 2            
            
            ledHSVColour = availableColours[selectedColourPos]    
            ledRGBColour = convertHSVtoRGB(ledHSVColour)
            
            strip.clear_strip()
            strip.set_pixel_rgb(ledOne, ledRGBColour, 5)
            if ledTwo < 61: strip.set_pixel_rgb(ledTwo, ledRGBColour)
            if ledThree < 61: strip.set_pixel_rgb(ledThree, ledRGBColour, 5)
            strip.show()
            time.sleep(delay)
            
        for x in range(60, 0, -1):
            ledOne = x
            ledTwo = x - 1
            ledThree = x - 2            
            
            ledHSVColour = availableColours[selectedColourPos]    
            ledRGBColour = convertHSVtoRGB(ledHSVColour)
            
            strip.clear_strip()
            strip.set_pixel_rgb(ledOne, ledRGBColour, 5)
            if ledTwo < 0: strip.set_pixel_rgb(ledTwo, ledRGBColour)
            if ledThree < 0: strip.set_pixel_rgb(ledThree, ledRGBColour, 5)
            strip.show()
            time.sleep(delay)


def simButton():
    count = 0
    while count < 6:
        buttonColour()
        time.sleep(0.3)
        count = count +1


print("Simulate pressing button to change colour")
t1 = threading.Thread(target=simButton)
t1.start()
time.sleep(5)
endThread()
strip.clear_strip()

print("Fast Rainbow")
t1 = threading.Thread(target=rainbow, args=(1,))
t1.start()
time.sleep(5)
endThread()
strip.clear_strip()

#strip.clear_strip()
#time.sleep(2)

#print("Slow Rainbow")
#rainbow(0.1)

#strip.clear_strip()
#time.sleep(2)

#print("Rotate")
#rotateLEDs(0.1) #slow rotate

#strip.clear_strip()
#time.sleep(2)

#rotateLEDs(0.01) #fast rotate

strip.clear_strip()
strip.cleanup()
