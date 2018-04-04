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


ledRGBColoura = convertHSVtoRGB(60)
ledRGBColourb = convertHSVtoRGB(120)
ledRGBColourc = convertHSVtoRGB(250)

#while True:

minBrightness = 1
maxBrightness = 30

for fadeBrightness in range(minBrightness, maxBrightness):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColoura, fadeBrightness)        
    strip.show()
    time.sleep(0.01)
        
for fadeBrightness in range(maxBrightness, minBrightness, -1):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColoura, fadeBrightness)        
    strip.show()
    time.sleep(0.01)

for fadeBrightness in range(minBrightness, maxBrightness):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColourb, fadeBrightness)        
    strip.show()
    time.sleep(0.01)
        
for fadeBrightness in range(maxBrightness, minBrightness, -1):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColourb, fadeBrightness)        
    strip.show()
    time.sleep(0.01)
    
for fadeBrightness in range(minBrightness, maxBrightness):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColourc, fadeBrightness)        
    strip.show()
    time.sleep(0.01)
        
for fadeBrightness in range(maxBrightness, minBrightness, -1):
    for ledID in range(0, 60):
        strip.set_pixel_rgb(ledID, ledRGBColourc, fadeBrightness)        
    strip.show()
    time.sleep(0.01)
    
    strip.clear_strip()
    #time.sleep(5)
