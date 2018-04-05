#!/usr/bin/env python3

# Imports
import time
import datetime
import threading

global bedTime

bedTime = False

def checkTime():
    global bedTime
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
    
        if timeNowHHmm >= timeOnHHmm and timeNowHHmm <= timeOffHHmm:
            bedTime = True
        else:
            bedTime = False

tBed = threading.Thread(name="checkBedTime", target=checkTime)
tBed.start()
    
while True:
    
    timeNow = datetime.datetime.now()
    timeNowHHmm = timeNow.strftime("%H:%M")
    print(bedTime, " - ", timeNowHHmm)
