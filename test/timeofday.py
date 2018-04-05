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
print(timeOn)
print(timeOnHHmm)

timeOff = datetime.datetime.strptime("19:00", "%H:%M")
print(timeOff)
