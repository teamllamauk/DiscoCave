#!/usr/bin/env python3

# Imports
import time
import datetime

def checkTime():
    #wakeUp = "07:00"
    #goToBed = "19:00"
    
    wakeUp = "10:36"
    goToBed = "10:38"
    
    timeNow = datetime.datetime.now()
    timeNowHHmm = timeNow.strftime("%H:%M")
    
    timeOn = datetime.datetime.strptime(wakeUp, "%H:%M")
    timeOnHHmm = timeOn.strftime("%H:%M")
    
    timeOff = datetime.datetime.strptime(goToBed, "%H:%M")
    timeOffHHmm = timeOff.strftime("%H:%M")
    
    if timeNowHHmm > timeOnHHmm and timeNowHHmm < timeOffHHmm:
        return True
    else:
        return False

while True:
    
    timeNow = datetime.datetime.now()
    timeNowHHmm = timeNow.strftime("%H:%M")
    print(checkTime(), " - ", timeNowHHmm)
