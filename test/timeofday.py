#!/usr/bin/env python3

# Imports
import time
import datetime


timeNow = datetime.datetime.now().time()
print(timeNow)

timeHHmm = datetime.datetime.strptime(timeNow, "%H:%M")
print(timeHHmm)



#def timeDiff():
    
