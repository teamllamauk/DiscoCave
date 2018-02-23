#!/usr/bin/env python3

import sys
import time
import colorsys

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rgb')
#strip = apa102.APA102(num_led=60, global_brightness=5, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

global availableColours
global selectedColourPos

availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
selectedColourPos = 11

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

    
def solidColour():
    global availableColours
    global selectedColourPos
    
    selectedColourPos = selectedColourPos + 1
    if selectedColourPos > 11: selectedColourPos = 0
    
    ledHSVColour = availableColours[selectedColourPos]
    
    ledHSVColour = availableColours
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledRGBColour)
        #strip.set_pixel_rgb(LED ID, RGB Colour, Brightness ie 5 = 5%)
    strip.show()
   
def slowRainbow():
    count = 0
    while count < 360:
        solidColour(count)
        time.sleep(1)
        count = count + 30
        
def fastRainbow():
    count = 0
    while count < 360:
        solidColour(count)
        time.sleep(0.1)
        count = count + 30
        
def rotateLEDs():
    strip.set_pixel_rgb(0, 0xFF0000)
    strip.set_pixel_rgb(1, 0xFF0000, 5)
    strip.set_pixel_rgb(2, 0xFF0000)
    strip.rotate()
    time.sleep(5)

print("Simulate pressing button to change colour")
count = 0
while count < 20:
    solidColour()
    time.sleep(0.3)

print("Fast Rainbow")
fastRainbow()

print("Slow Rainbow")
slowRainbow()

print("Rotate")
rotateLEDs()

strip.clear_strip()
strip.cleanup()
