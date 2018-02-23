#!/usr/bin/env python3

import sys
import time
import colorsys

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

#strip = apa102.APA102(num_led=60, global_brightness=20, mosi = 10, sclk = 11, order='rgb')
strip = apa102.APA102(num_led=60, global_brightness=5, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

def convertHSVtoRGB(hsvColour):
    rgbColour = colorsys.hsv_to_rgb(hsvColour/360,1,1)
    print("HSV: ", hsvColour)
    print("RGB: ", rgbColour)
    print("R: ", rgbColour[0])
    print("G: ", rgbColour[1])
    print("B: ", rgbColour[2])    
    
    hR = int(rgbColour[0] * 256)
    if hR == 256: hR = 255
    rgbColour[0] = hR
        
    hG = int(rgbColour[1] * 256)
    if hG == 256: hG = 255
    rgbColour[1] = hG
    
    hB = int(rgbColour[2] * 256)
    if hB == 256: hB = 255
    rgbColour[2] = hB
    
    print("Rx: ", hR)
    print("Gx: ", hG)
    print("Bx: ", hB)
    print("R: ", rgbColour[0])
    print("G: ", rgbColour[1])
    print("B: ", rgbColour[2])

    
def solidColour(ledHSVColour):
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    #strip.clear_strip()
    #for x in range(0, 60):
    #    strip.set_pixel_rgb(x, ledRGBColour) 
    #strip.show()
   


count = 0
while count < 360:
    solidColour(count)
    time.sleep(1)
    count = count + 10
    

#solidColour(0xFF0000) #Red
#time.sleep(2)
#solidColour(0xFFA500) #Orange
#time.sleep(2)
#solidColour(0xFFFF00) #Yellow
#time.sleep(2)
#solidColour(0x00FF00) #Green
#time.sleep(2)
#solidColour(0x0000FF) #Blue
#time.sleep(2)
#solidColour(0x4B0082) #Indigo
#time.sleep(2)
#solidColour(0xEE82EE) #Violet
#time.sleep(2)

strip.clear_strip()
strip.cleanup()
