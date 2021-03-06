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
global brightness
global availableBrightness
global selectedColourPos
global availableColours
global killThread
global bounceRed
global bounceBlue
global bounceWhite

prevPowerMode = 0
powerMode = 0 # 0 is off, 1 is on
brightness = 3 # index of availableBrightness
availableBrightness = (8, 12, 16, 20)
selectedColourPos = 0 # index of availableColours
availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
killThread = False # kills running threads when set to true
bounceRed = time.time()
bounceBlue = time.time()
bounceWhite = time.time()

# button order: w,g,b,r,o

#btn_red_pin = 25        # Light Brightness
#btn_blue_pin = 27        # Light Colour
#btn_white_pin = 6       # Power On/Off
btn_red_pin = 23
btn_blue_pin = 24
btn_white_pin = 6

led_red_pin = 22
led_blue_pin = 25
led_white_pin = 5

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

rGPIO.setup(btn_red_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_blue_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_white_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.setup(led_blue_pin,rGPIO.OUT)
rGPIO.setup(led_white_pin,rGPIO.OUT)

rGPIO.output(led_red_pin,rGPIO.LOW)
rGPIO.output(led_blue_pin,rGPIO.LOW)
rGPIO.output(led_white_pin,rGPIO.LOW)

def endThread():
    global killThread        
    #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread)
    while threading.activeCount() > 1:        
        killThread = True
        #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Ending...")    
    killThread = False
    strip.clear_strip()
    #strip.cleanup()
    #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Stopped")

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
    global killThread              
    
    setSolidColour()
    
    start = time.time()
    while killThread == False:
        if time.time() - start >= 0.1:            
            setSolidColour()
            start = time.time()
            
            
def setSolidColour():
    global availableColours
    global selectedColourPos
    global availableBrightness
    global brightness
    global killThread
    
    ledHSVColour = availableColours[selectedColourPos]    
    ledRGBColour = convertHSVtoRGB(ledHSVColour)
    #strip.clear_strip()
    for x in range(0, 60):
        strip.set_pixel_rgb(x, ledRGBColour, availableBrightness[brightness])        
    strip.show()


def btn_Callback(button_pin):
    
    global powerMode
    global selectedMode
    global availableModes
    global brightness
    global availableBrightness
    global selectedColourPos
    global availableColours
    global killThread
    global bounceRed
    global bounceBlue
    global bounceWhite
    
    
    #print("callback button pin", button_pin)
    if button_pin == btn_red_pin:           # Red: Brightness        
        if time.time() - bounceRed >= 0.5:
            bounceRed = time.time()
            #print("brightness", powerMode)
            if powerMode == 1:
                maxBrightness = len(availableBrightness) - 1
                brightness = brightness + 1
                if brightness > maxBrightness:
                    brightness = 0            
                
                print("brightness : ", brightness)
                #rGPIO.output(led_red_pin,rGPIO.HIGH)            
                #rGPIO.output(led_red_pin,rGPIO.LOW)          
    
    elif button_pin == btn_blue_pin:        # Blue: Colour
        if time.time() - bounceBlue >= 0.5:
            bounceBlue = time.time()
            #print("colour", powerMode)
            if powerMode == 1:        
                maxSelectedColourPos = len(availableColours) - 1
                selectedColourPos = selectedColourPos + 1
                if selectedColourPos > maxSelectedColourPos:
                    selectedColourPos = 0            
            
                print("Colour Pos : ", selectedColourPos)
            #rGPIO.output(led_blue_pin,rGPIO.HIGH)            
            #rGPIO.output(led_blue_pin,rGPIO.LOW)
            
    elif button_pin == btn_white_pin:       # White: Power On/Off
         if time.time() - bounceWhite >= 0.5:
            bounceWhite = time.time()
            #print("o", powerMode)
            if powerMode == 0:        
                rGPIO.output(led_white_pin,rGPIO.HIGH)
                powerMode = 1
            else:
                rGPIO.output(led_white_pin,rGPIO.LOW)
                powerMode = 0


rGPIO.add_event_detect(btn_red_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)
rGPIO.add_event_detect(btn_blue_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)
rGPIO.add_event_detect(btn_white_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)

def runMode():
    #print("run mode")
    endThread()
    #if availableModes[selectedMode] == "solidColour":
    t1 = threading.Thread(target=solidColour)
    #elif availableModes[selectedMode] == "rainbow":
    #    t1 = threading.Thread(target=rainbow, args=(0.3,))
    #elif availableModes[selectedMode] == "rotateLEDs":
    #    t1 = threading.Thread(target=rotateLEDs, args=(0.01,))
    #elif availableModes[selectedMode] == "bounceLEDs":
    #    t1 = threading.Thread(target=bounceLEDs, args=(0.01,))
    t1.start()

while True:
    #print("Thread count: ", threading.activeCount())
    if powerMode == 0 and prevPowerMode == 1:
        print("Power off")
        endThread()
        prevPowerMode = 0
        strip.clear_strip()
        #strip.cleanup()
        
    elif powerMode == 1 and prevPowerMode == 0:
        print("Power on")
        prevPowerMode = 1       
        runMode()
