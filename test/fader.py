#!/usr/bin/env python3

# Imports
import sys
import time
import threading
import colorsys
import RPi.GPIO as rGPIO

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=30, mosi = 10, sclk = 11, order='rgb')
strip.clear_strip()

global brightness
global availableBrightness
global selectedColourPos
global availableColours

brightness = 2 # index of availableBrightness
availableBrightness = (7, 14, 20)
selectedColourPos = 0 # index of availableColours
availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)

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

def setSolidColour(brightnessOveride):
    global availableColours
    global selectedColourPos
    global availableBrightness
    global brightness
    
    ledStripBrightness = availableBrightness[brightness]
    
    if brightnessOveride > -1:
        ledStripBrightness = brightnessOveride
    
    ledHSVColour = availableColours[selectedColourPos]    
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    #strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledRGBColour, ledStripBrightness)        
    strip.show()


def fader(delayMs, minBrightness, maxBrightness):    
    delay = delayMs / 1000
    for a in range(0, 5):
        for fadeBrightness in range(minBrightness, maxBrightness):
            #for ledID in range(0, 60):
            #    strip.set_pixel_rgb(ledID, ledRGBColour, fadeBrightness)        
            #strip.show()
            setSolidColour(fadeBrightness)
            time.sleep(delay)
        
        for fadeBrightness in range(maxBrightness, minBrightness, -1):
            setSolidColour(fadeBrightness)
            time.sleep(delay)


ledRGBColour = convertHSVtoRGB(60)


#while True:

#minBrightness = 1
#maxBrightness = 30
#delaytimeMs = 10
#delaytime = delaytimeMs / 1000

#print(delaytime)

fader(10, 1, 30)

#for a in range(0, 5):
#    for fadeBrightness in range(minBrightness, maxBrightness):
#        for ledID in range(0, 60):
#            strip.set_pixel_rgb(ledID, ledRGBColour, fadeBrightness)        
#        strip.show()
#        time.sleep(delaytime)
#        
#    for fadeBrightness in range(maxBrightness, minBrightness, -1):
#        for ledID in range(0, 60):
#            strip.set_pixel_rgb(ledID, ledRGBColour, fadeBrightness)        
#        strip.show()
#        time.sleep(delaytime)

    
    
strip.clear_strip()
#time.sleep(5)
