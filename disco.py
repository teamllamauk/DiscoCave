#!/usr/bin/env python3

# Imports
import sys
import time
import datetime
import threading
import colorsys
import pygame
import RPi.GPIO as rGPIO
from random import randint
#webserver imports
import string,cgi 
from os import curdir, sep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


sys.path.insert(0, '/home/pi/Development/APA102_Pi')
import apa102

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            try:
                url_addr, query_string = self.path.split("?")
            except:
                url_addr = self.path
                query_string = ""
            if url_addr == "/":
                url_addr = "index.html"
            try:
                query = urlparse(self.path).query
                query_components = dict(qc.split("=") for qc in query.split("&"))
                qGpio = query_components["gpio"]
                print ('gpio: -', qGpio,'-')
                if qGpio == '1':
                    print('gpio white button')
                    whiteButton()
            except:
                print ("no qGpio")
            f = open(curdir + sep + url_addr)
            self.send_response(200)
            self.send_header('Content-type',    'text/html')
            self.end_headers()
            self.wfile.write(bytes(f.read(), "utf-8"))
            f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % url_addr)


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
global btn_orange_flag

btn_orange_flag = 0
prevPowerMode = 0
bedTime = False
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
btn_red_pin = 13
btn_blue_pin = 24
btn_white_pin = 17
btn_green_pin = 23
btn_orange_pin = 6

led_red_pin = 12
led_blue_pin = 25
led_white_pin = 27
led_green_pin = 22
led_orange_pin = 5

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)

rGPIO.setup(btn_red_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_blue_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_white_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_green_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)
rGPIO.setup(btn_orange_pin, rGPIO.IN, pull_up_down=rGPIO.PUD_UP)

rGPIO.setup(led_red_pin,rGPIO.OUT)
rGPIO.setup(led_blue_pin,rGPIO.OUT)
rGPIO.setup(led_white_pin,rGPIO.OUT)
rGPIO.setup(led_green_pin,rGPIO.OUT)
rGPIO.setup(led_orange_pin,rGPIO.OUT)

rGPIO.output(led_red_pin,rGPIO.LOW)
rGPIO.output(led_blue_pin,rGPIO.LOW)
rGPIO.output(led_white_pin,rGPIO.LOW)
rGPIO.output(led_green_pin,rGPIO.LOW)
rGPIO.output(led_orange_pin,rGPIO.LOW)

def endThread():
    global killThread        
    #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread)
    while threading.activeCount() > 1:        
        killThread = True
        #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Ending...")
        keepLooping = False
        for t in threading.enumerate():            
            if t.getName() == "lightAffect": keepLooping = True            
        if keepLooping == False: break
        
    killThread = False
    strip.clear_strip()
    #strip.cleanup()
    #print("End Thread! ", "Thread Count: ", threading.activeCount(), ", KillThread = ", killThread, ", Stopped")



def whiteButton():
    global powerMode
    global prevPowerMode
    print('white button function')
    print('white button power mode: ', powerMode)
    if powerMode == 0:
        rGPIO.output(led_white_pin,rGPIO.HIGH)
        powerMode = 1
    else:
        rGPIO.output(led_white_pin,rGPIO.LOW)
        powerMode = 0

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
    #print("Solid")
    setSolidColour(-1)    
    start = time.time()
    while killThread == False:
        #print("run solid: killTread = ", killThread, ". Active threads = ", threading.activeCount())
        if time.time() - start >= 0.1:            
            setSolidColour(-1)
            start = time.time()
    #print("end solid")
            
            
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
    #print("Rainbow")
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
    #print("Rotate")
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
    #print("    Bounce")
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
    global btn_orange_flag
    
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
    elif button_pin == btn_orange_pin:
        if powerMode == 1:
            if btn_orange_flag == 0 :
                ts = threading.Thread(name="soundclip", target=playSound)
                ts.start()
            #else :
                #print("Already Playing")
            
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
                whiteButton()
                
                #if powerMode == 0:        
                #    rGPIO.output(led_white_pin,rGPIO.HIGH)
                #    powerMode = 1
                #else:
                #    rGPIO.output(led_white_pin,rGPIO.LOW)
                #    powerMode = 0
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
rGPIO.add_event_detect(btn_orange_pin, rGPIO.RISING, callback=btn_Callback, bouncetime=200)

def checkTime():
    global bedTime
    global powerMode
    
    wakeUp = "00:01"
    #goToBed = "19:15"   
    goToBed = "23:59"
    
    while True:
    
        timeNow = datetime.datetime.now()
        timeNowHHmm = timeNow.strftime("%H:%M")
    
        timeOn = datetime.datetime.strptime(wakeUp, "%H:%M")
        timeOnHHmm = timeOn.strftime("%H:%M")
    
        timeOff = datetime.datetime.strptime(goToBed, "%H:%M")
        timeOffHHmm = timeOff.strftime("%H:%M")
    
        #print("Now: ", timeNowHHmm, ", On: ", timeOnHHmm, ", Off: ", timeOffHHmm)
        
        if timeNowHHmm >= timeOnHHmm and timeNowHHmm <= timeOffHHmm:
            bedTime = False            
        else:
            bedTime = True
            powerMode = 0
        
        #print("Checktime: ", bedTime)
        time.sleep(15)

def illuminateButtonPress():
    global bedTime
    global powerMode
    
    while True:
        if bedTime == False and powerMode == 1:
            #print("Red Button State: ", rGPIO.input(btn_red_pin))
            if rGPIO.input(btn_red_pin) == 0:
                rGPIO.output(led_red_pin,rGPIO.HIGH)
            else:
                rGPIO.output(led_red_pin,rGPIO.LOW)
                
            if rGPIO.input(btn_blue_pin) == 0:
                rGPIO.output(led_blue_pin,rGPIO.HIGH)
            else:
                rGPIO.output(led_blue_pin,rGPIO.LOW)
                
            if rGPIO.input(btn_green_pin) == 0:
                rGPIO.output(led_green_pin,rGPIO.HIGH)
            else:
                rGPIO.output(led_green_pin,rGPIO.LOW)
        

def playSound():
    global btn_orange_flag
    #print("Start Sound")
    btn_orange_flag = 1
    
    pygame.mixer.init()
    volume = pygame.mixer.music.get_volume()
    #print(volume)
    
    audio_rand = randint(1, 7)    # Pick a random number between 1 and 25.
    
    if audio_rand == 7 :
        sound_file = "/home/pi/Development/DiscoCave/audio/vegimal.mp3"
        print("veg")
    else :
        sound_file = "/home/pi/Development/DiscoCave/audio/octoalert.mp3"
        print("octo")
        
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy() == True:
        rGPIO.output(led_orange_pin,rGPIO.HIGH)
        time.sleep(0.25)
        rGPIO.output(led_orange_pin,rGPIO.LOW)
        time.sleep(0.25)
    
    rGPIO.output(led_orange_pin,rGPIO.LOW)
    #print("Finished Sound")
    btn_orange_flag = 0


def runMode():
    print("run mode , ", availableModes[selectedMode])
    endThread()
    #print("run 1")
    if killThread == False:
        if availableModes[selectedMode] == "solidColour":
            #print("run 2")
            t1 = threading.Thread(name="lightAffect", target=solidColour)
            t1.start()
        elif availableModes[selectedMode] == "rainbow":
            #print("run 3")
            t1 = threading.Thread(name="lightAffect", target=rainbow, args=(0.3,))
            t1.start()
        elif availableModes[selectedMode] == "rotateLEDs":
            #print("run 4")
            t1 = threading.Thread(name="lightAffect", target=rotateLEDs, args=(0.01,))
            t1.start()
        elif availableModes[selectedMode] == "bounceLEDs":
            #print("run 5")
            t1 = threading.Thread(name="lightAffect", target=bounceLEDs, args=(0.00001,))
            t1.start()
        elif availableModes[selectedMode] == "fader":
            #print("run 5")
            t1 = threading.Thread(name="lightAffect", target=fader, args=(10, 1, 30,))
            t1.start()

powerMode = 0
print("Started")
#tBed = threading.Thread(name="checkBedTime", target=checkTime)
#tBed.start()

tIllume = threading.Thread(name="illuminate", target=illuminateButtonPress)
tIllume.start()


server = HTTPServer(('', 80), MyHandler)
print ('started httpserver...')
server.serve_forever()
#    except KeyboardInterrupt:
#        print ('stopping server')
#        server.socket.close()


#if __name__ == '__main__':
#    main()



while True:
    #bedTime = checkTime
    
    #print("Thread count: ", threading.activeCount())
    #for t in threading.enumerate():
    #    print("    Thread Name: ", t.getName())
    #    time.sleep(0.5)
        
    #print("Bedtime - ", bedTime)
    
    if powerMode == 0 and prevPowerMode == 1:
        print("Power off - while loop")
        #endThread()
        #prevPowerMode = 0
        #strip.clear_strip()
        #strip.cleanup()        
    elif powerMode == 1 and prevPowerMode == 0:
        print("Power on - while loop")
        #prevPowerMode = 1       
        #runMode()
