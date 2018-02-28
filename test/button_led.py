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

strip.clear_strip()

global prevPowerMode
global powerMode
global selectedMode
global availableModes
global brightness
global availableBrightness
global selectedColourPos
global availableColours
global killThread

prevPowerMode = 0
powerMode = 0 # 0 is off, 1 is on
selectedMode = 0 # index of availableModes
availableModes = ("solidColour", "rainbow", "rotateLEDs", "bounceLEDs")
brightness = 3 # index of availableBrightness
availableBrightness = (8, 12, 16, 20)
selectedColourPos = 0 # index of availableColours
availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
killThread = False # kills running threads when set to true

# button order: w,g,b,r,o

btn_red_pin = 25        # Light Brightness
btn_green_pin = 12      # Light Mode
btn_blue_pin = 7        # Light Colour
btn_orange_pin = 23     # Activate Sounds
btn_white_pin = 6       # Power On/Off

led_red_pin = 8
led_green_pin = 5
led_blue_pin = 1
led_orange_pin = 24
led_white_pin = 13

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

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

def endThread():
    global killThread    
    print(threading.activeCount())
    while threading.activeCount() > 1:
        killThread = True
        #print("Ending...")
    
    killThread = False
    print("Thread Stopped")

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
    print("    Solid Colour")        
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    
    #strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledRGBColour, availableBrightness[brightness])        
    strip.show()


def rainbow(delay):
    global availableColours
    global selectedColourPos
    global killThread  
    
    start = time.time()
    while killThread == False:
        if time.time() - start >= delay:
            print("    Rainbow")
            solidColour(availableColours[selectedColourPos])
            selectedColourPos = selectedColourPos + 1
            if selectedColourPos > 11: selectedColourPos = 0
            start = time.time()
            #time.sleep(delay)


def rotateLEDs(delay):
    global availableColours
    global selectedColourPos    
    global killThread
    
    start = time.time()
    while killThread == False:
        print("    Rotate")
        #for x in range(0, 60):
        x = 0    
        while x < 60 and killThread == False:            
            if time.time() - start >= delay:
                print("        rotating")
                ledOne = x
                ledTwo = x + 1
                ledThree = x + 2            
            
                ledHSVColour = availableColours[selectedColourPos]    
                ledRGBColour = convertHSVtoRGB(ledHSVColour)
                
                dimmedBrightness = availableBrightness[brightness] / 4                
            
                strip.clear_strip()
                strip.set_pixel_rgb(ledOne, ledRGBColour, dimmedBrightness)
                if ledTwo < 61: strip.set_pixel_rgb(ledTwo, ledRGBColour, availableBrightness[brightness])
                if ledThree < 61: strip.set_pixel_rgb(ledThree, ledRGBColour, dimmedBrightness)
                strip.show()
                x = x + 1
                start = time.time()
            #time.sleep(delay)


def bounceLEDs(delay):    
    global availableColours
    global selectedColourPos
    global killThread
    
    start = time.time()
    while killThread == False:
        print("    Bounce")
        x = 0    
        while x < 60 and killThread == False:
            if time.time() - start >= delay:
                print("        Bounce F")
                ledOne = x
                ledTwo = x + 1
                ledThree = x + 2            
            
                ledHSVColour = availableColours[selectedColourPos]    
                ledRGBColour = convertHSVtoRGB(ledHSVColour)
                
                dimmedBrightness = availableBrightness[brightness] / 4
            
                strip.clear_strip()
                strip.set_pixel_rgb(ledOne, ledRGBColour, dimmedBrightness)
                if ledTwo < 61: strip.set_pixel_rgb(ledTwo, ledRGBColour, availableBrightness[brightness])
                if ledThree < 61: strip.set_pixel_rgb(ledThree, ledRGBColour, dimmedBrightness)
                strip.show()
                x = x + 1
                start = time.time()            
            
        while x > 0 and killThread == False:
            if time.time() - start >= delay:
                print("        Bounce R")
                ledOne = x
                ledTwo = x - 1
                ledThree = x - 2            
            
                ledHSVColour = availableColours[selectedColourPos]    
                ledRGBColour = convertHSVtoRGB(ledHSVColour)
                
                dimmedBrightness = availableBrightness[brightness] / 4
            
                strip.clear_strip()
                strip.set_pixel_rgb(ledOne, ledRGBColour, dimmedBrightness)
                if ledTwo > 0: strip.set_pixel_rgb(ledTwo, ledRGBColour, availableBrightness[brightness])
                if ledThree > 0: strip.set_pixel_rgb(ledThree, ledRGBColour, dimmedBrightness)
                strip.show()
                x = x - 1
                start = time.time()


#def simButton():
#    count = 0
#    while count < 6:
#        buttonColour()
#        time.sleep(0.3)
#        count = count +1


def btn_Callback(button_pin):
    
    global powerMode
    global selectedMode
    global availableModes
    global brightness
    global availableBrightness
    global selectedColourPos
    global availableColours
    global killThread
    
    print (button_pin)
    if button_pin == btn_red_pin:           # Red: Brightness
        if powerMode == 1:
            maxBrightness = len(availableBrightness) - 1
            brightness = brightness + 1
            if brightness > maxBrightness:
                maxBrightness = 0
        
            #rGPIO.output(led_red_pin,rGPIO.HIGH)            
            #rGPIO.output(led_red_pin,rGPIO.LOW)
            
    elif button_pin == btn_green_pin:       # Green: Change Mode
        if powerMode == 1:
            maxSelectedMode = len(availableModes) - 1
            selectedMode = selectedMode + 1
            if selectedMode > maxSelectedMode:
                selectedMode = 0
            
            runMode()            
                        
            #rGPIO.output(led_green_pin,rGPIO.HIGH)            
            #rGPIO.output(led_green_pin,rGPIO.LOW)
                
    elif button_pin == btn_blue_pin:        # Blue: Colour
        if powerMode == 1:        
            maxSelectedColourPos = len(availableColours) - 1
            selectedColourPos = selectedColourPos + 1
            if selectedColourPos > maxSelectedColourPos:
                selectedColourPos = 0            
            
            #rGPIO.output(led_blue_pin,rGPIO.HIGH)            
            #rGPIO.output(led_blue_pin,rGPIO.LOW)
            
    elif button_pin == btn_orange_pin:      # Orange: Sounds
        a = 1 # dummy assignment to stop error on empty elif
        #rGPIO.output(led_orange_pin,rGPIO.HIGH)            
        #rGPIO.output(led_orange_pin,rGPIO.LOW)
            
    elif button_pin == btn_white_pin:       # White: Power On/Off
        if powerMode == 0:        
            rGPIO.output(led_white_pin,rGPIO.HIGH)
            powerMode = 1
        else:
            rGPIO.output(led_white_pin,rGPIO.LOW)
            powerMode = 0


rGPIO.add_event_detect(btn_red_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_green_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_blue_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_orange_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)
rGPIO.add_event_detect(btn_white_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=500)


#print("Simulate pressing button to change colour")
#t1 = threading.Thread(target=simButton)
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("Slow Rainbow")
#t1 = threading.Thread(target=rainbow, args=(1,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("Fast Rainbow")
#t1 = threading.Thread(target=rainbow, args=(0.1,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("slow rotate")
#t1 = threading.Thread(target=rotateLEDs, args=(0.1,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("fast rotate")
#t1 = threading.Thread(target=rotateLEDs, args=(0.01,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("Slow Bounce")
#t1 = threading.Thread(target=bounceLEDs, args=(0.1,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#print("fast Bounce")
#t1 = threading.Thread(target=bounceLEDs, args=(0.01,))
#t1.start()
#time.sleep(5)
#endThread()
#strip.clear_strip()

#strip.clear_strip()
#strip.cleanup()

def runMode():
    print("run mode")
    endThread()
    if availableModes[selectedMode] == "solidColour":
        t1 = threading.Thread(target=buttonColour)
    elif availableModes[selectedMode] == "rainbow":
        t1 = threading.Thread(target=rainbow, args=(0.3,))
    elif availableModes[selectedMode] == "rotateLEDs":
        t1 = threading.Thread(target=rotateLEDs, args=(0.01,))
    elif availableModes[selectedMode] == "bounceLEDs":
        t1 = threading.Thread(target=bounceLEDs, args=(0.01,))
    t1.start()

while True:
    if powerMode == 0 and prevPowerMode == 1:
        killThread = 1
        prevPowerMode = 0
        strip.clear_strip()
        strip.cleanup()
        
    elif powerMode == 1 and prevPowerMode == 0:
        prevPowerMode = 1       
        runMode()
