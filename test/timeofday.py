#!/usr/bin/env python3

# Imports
import time
import datetime


timeNow = datetime.datetime.now()
print(timeNow)

timeNowHHmm = timeNow.strftime("%H:%M")
print(timeNowHHmm)

timeOn = datetime.datetime.strptime("07:00", "%H:%M")
timeOnHHmm = timeOn.strftime("%H:%M")
print(timeOnHHmm)

timeOff = datetime.datetime.strptime("19:00", "%H:%M")
timeOffHHmm = timeOff.strftime("%H:%M")
print(timeOffHHmm)

if timeNowHHmm > timeOnHHmm and timeNowHHmm < timeOffHHmm:
    print("OK")
