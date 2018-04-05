#!/usr/bin/env python3

# Imports
import sys
import time
import datetime
import threading
import colorsys
import RPi.GPIO as rGPIO

sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

strip = apa102.APA102(num_led=60, global_brightness=30, mosi = 10, sclk = 11, order='rgb')

strip.clear_strip()

global prevPowerMode
global bedTime
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
global bounceGreen

prevPowerMode = 0
bedTime = True
powerMode = 0 # 0 is off, 1 is on
selectedMode = 0 # index of availableModes
availableModes = ("solidColour", "rainbow", "rotateLEDs", "fader", "bounceLEDs")
brightness = 2 # index of availableBrightness
availableBrightness = (1, 15, 30)
selectedColourPos = 0 # index of availableColours
availableColours = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
killThread = False # kills running threads when set to true
bounceRed = time.time()
bounceBlue = time.time()
bounceWhite = time.time()
bounceGreen = time.time()

# button order: w,g,b,r,o

#btn_red_pin = 25        # Light Brightness
#btn_blue_pin = 27        # Light Colour
#btn_white_pin = 6       # Power On/Off
btn_red_pin = 23
btn_blue_pin = 24
btn_white_pin = 6
btn_green_pin = 13

led_red_pin = 22
led_blue_pin = 25
led_white_pin = 5
led_green_pin = 12

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

rGPIO.setup(btn_red_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_blue_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_white_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_green_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.setup(led_blue_pin,rGPIO.OUT)
rGPIO.setup(led_white_pin,rGPIO.OUT)
rGPIO.setup(led_green_pin,rGPIO.OUT)

rGPIO.output(led_red_pin,rGPIO.LOW)
rGPIO.output(led_blue_pin,rGPIO.LOW)
rGPIO.output(led_white_pin,rGPIO.LOW)
rGPIO.output(led_green_pin,rGPIO.LOW)

def endThread():
    global killThread        
    print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread)
    while threading.activeCount() > 1:        
        killThread = True
        print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Ending...")
        keepLooping = False
        for t in threading.enumerate():            
            if t.getName() == "lightAffect": keepLooping = True            
        if keepLooping == False: break
        
    killThread = False
    strip.clear_strip()
    #strip.cleanup()
    print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Stopped")


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
    print("Solid")
    setSolidColour(-1)    
    start = time.time()
    while killThread == False:
        #print("run solid: killTread = ", killThread, ". Active threads = ", threading.activeCount())
        if time.time() - start >= 0.1:            
            setSolidColour(-1)
            start = time.time()
    print("end solid")
            
            
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

 
def rainbow(delay):
    global availableColours
    global selectedColourPos
    global killThread  
    print("Rainbow")
    start = time.time()
    while killThread == False:
        if time.time() - start >= delay:            
            setSolidColour(-1)            
            selectedColourPos = selectedColourPos + 1
            if selectedColourPos > 11: selectedColourPos = 0
            start = time.time()


def fader(delayMs, minBrightness, maxBrightness): 
    global killThread
    
    delay = delayMs / 1000    
    fadeDir = 1 # 1 = fade up, 0 = fade down
    fadeBrightness = minBrightness
    start = time.time()
    while killThread == False:
        if time.time() - start >= delay:                   
            setSolidColour(fadeBrightness)
            start = time.time()
            if fadeDir == 1:
                fadeBrightness = fadeBrightness + 1
                if fadeBrightness == maxBrightness:
                    fadeDir = 0
            elif fadeDir == 0:
                fadeBrightness = fadeBrightness - 1
                if fadeBrightness == minBrightness:
                    fadeDir = 1


def rotateLEDs(delay):
    global availableColours
    global selectedColourPos    
    global killThread
    print("Rotate")
    start = time.time()
    while killThread == False:
        #print("Rotate")
        #for x in range(0, 60):
        x = 0    
        while x < 60 and killThread == False:            
            if time.time() - start >= delay:
                #print("        rotating")
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


def bounceLEDs(delay):    
    global availableColours
    global selectedColourPos
    global killThread
    print("    Bounce")
    start = time.time()
    while killThread == False:
        
        x = 0    
        while x < 60 and killThread == False:
            if time.time() - start >= delay:
                #print("        Bounce F")
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
                #print("        Bounce R")
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
    global bounceGreen
    
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
                
                #print("brightness : ", brightness)
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
            
                #print("Colour Pos : ", selectedColourPos)
            #rGPIO.output(led_blue_pin,rGPIO.HIGH)            
            #rGPIO.output(led_blue_pin,rGPIO.LOW)
    elif button_pin == btn_green_pin:       # Green: Change Colour Mode
        if time.time() - bounceGreen >= 0.5:
            bounceGreen = time.time()
            if powerMode == 1:
                maxSelectedMode = len(availableModes) - 1
                selectedMode = selectedMode + 1
                if selectedMode > maxSelectedMode:
                    selectedMode = 0            
                runMode()            
        
    elif button_pin == btn_white_pin:       # White: Power On/Off
         if time.time() - bounceWhite >= 0.5:
            bounceWhite = time.time()
            #print("o", powerMode)
            if bedTime == False:
                if powerMode == 0:        
                    rGPIO.output(led_white_pin,rGPIO.HIGH)
                    powerMode = 1
                else:
                    rGPIO.output(led_white_pin,rGPIO.LOW)
                    powerMode = 0
            else:
                rGPIO.output(led_white_pin,rGPIO.HIGH)
                rGPIO.output(led_red_pin,rGPIO.HIGH)
                rGPIO.output(led_blue_pin,rGPIO.HIGH)
                rGPIO.output(led_green_pin,rGPIO.HIGH)
                rGPIO.output(led_orange_pin,rGPIO.HIGH)
                time.sleep(0.2)
                rGPIO.output(led_white_pin,rGPIO.LOW)
                rGPIO.output(led_red_pin,rGPIO.LOW)
                rGPIO.output(led_blue_pin,rGPIO.LOW)
                rGPIO.output(led_green_pin,rGPIO.LOW)
                rGPIO.output(led_orange_pin,rGPIO.LOW)
                time.sleep(0.2)
                rGPIO.output(led_white_pin,rGPIO.HIGH)
                rGPIO.output(led_red_pin,rGPIO.HIGH)
                rGPIO.output(led_blue_pin,rGPIO.HIGH)
                rGPIO.output(led_green_pin,rGPIO.HIGH)
                rGPIO.output(led_orange_pin,rGPIO.HIGH)
                time.sleep(0.2)
                rGPIO.output(led_white_pin,rGPIO.LOW)
                rGPIO.output(led_red_pin,rGPIO.LOW)
                rGPIO.output(led_blue_pin,rGPIO.LOW)
                rGPIO.output(led_green_pin,rGPIO.LOW)
                rGPIO.output(led_orange_pin,rGPIO.LOW)
                time.sleep(0.2)
                rGPIO.output(led_white_pin,rGPIO.HIGH)
                rGPIO.output(led_red_pin,rGPIO.HIGH)
                rGPIO.output(led_blue_pin,rGPIO.HIGH)
                rGPIO.output(led_green_pin,rGPIO.HIGH)
                rGPIO.output(led_orange_pin,rGPIO.HIGH)
                time.sleep(0.2)
                rGPIO.output(led_white_pin,rGPIO.LOW)
                rGPIO.output(led_red_pin,rGPIO.LOW)
                rGPIO.output(led_blue_pin,rGPIO.LOW)
                rGPIO.output(led_green_pin,rGPIO.LOW)
                rGPIO.output(led_orange_pin,rGPIO.LOW)
                

rGPIO.add_event_detect(btn_red_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)
rGPIO.add_event_detect(btn_blue_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)
rGPIO.add_event_detect(btn_white_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)
rGPIO.add_event_detect(btn_green_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)

def checkTime():
    global bedTime
    global powerMode
    #wakeUp = "07:00"
    #goToBed = "19:00"
    
    wakeUp = "10:54"
    goToBed = "10:55"
    
    while True:
    
        timeNow = datetime.datetime.now()
        timeNowHHmm = timeNow.strftime("%H:%M")
    
        timeOn = datetime.datetime.strptime(wakeUp, "%H:%M")
        timeOnHHmm = timeOn.strftime("%H:%M")
    
        timeOff = datetime.datetime.strptime(goToBed, "%H:%M")
        timeOffHHmm = timeOff.strftime("%H:%M")
    
        print("Now: ", timeNowHHmm, ", On: ", timeOnHHmm, ", Off: ", timeOffHHmm)
        
        if timeNowHHmm >= timeOnHHmm and timeNowHHmm <= timeOffHHmm:
            bedTime = True
            powerMode = 0
        else:
            bedTime = False
        
        print("Checktime: ", bedTime)
        time.sleep(15)


def runMode():
    print("run mode , ", availableModes[selectedMode])
    endThread()
    print("run 1")
    if killThread == False:
        if availableModes[selectedMode] == "solidColour":
            print("run 2")
            t1 = threading.Thread(name="lightAffect", target=solidColour)
            t1.start()
        elif availableModes[selectedMode] == "rainbow":
            print("run 3")
            t1 = threading.Thread(name="lightAffect", target=rainbow, args=(0.3,))
            t1.start()
        elif availableModes[selectedMode] == "rotateLEDs":
            print("run 4")
            t1 = threading.Thread(name="lightAffect", target=rotateLEDs, args=(0.01,))
            t1.start()
        elif availableModes[selectedMode] == "bounceLEDs":
            print("run 5")
            t1 = threading.Thread(name="lightAffect", target=bounceLEDs, args=(0.01,))
            t1.start()
        elif availableModes[selectedMode] == "fader":
            print("run 5")
            t1 = threading.Thread(name="lightAffect", target=fader, args=(10, 1, 30,))
            t1.start()
    
tBed = threading.Thread(name="checkBedTime", target=checkTime)
tBed.start()    

while True:
    #bedTime = checkTime
    
    print("Thread count: ", threading.activeCount())
    for t in threading.enumerate():
        print("    Thread Name: ", t.getName())
        time.sleep(0.5)
        
    print("Bedtime - ", bedTime)
    
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
