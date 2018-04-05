#!/usr/bin/env python3

# Imports
import time
import datetime

def checkTime():
    timeNow = datetime.datetime.now()
    timeNowHHmm = timeNow.strftime("%H:%M")
    
    timeOn = datetime.datetime.strptime("07:00", "%H:%M")
    timeOnHHmm = timeOn.strftime("%H:%M")
    
    timeOff = datetime.datetime.strptime("19:00", "%H:%M")
    timeOffHHmm = timeOff.strftime("%H:%M")
    
    if timeNowHHmm > timeOnHHmm and timeNowHHmm < timeOffHHmm:
        return True
    else
        return False

    
print(checkTime())
