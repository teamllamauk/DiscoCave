#!/usr/bin/env python3

import RPi.GPIO as rGPIO
import threading
import time

rGPIO.setmode(rGPIO.BCM)
rGPIO.setwarnings(False)
rGPIO.cleanup()

global killThread
killThread = False


def startThread():
    print("Start Thread")
    t1 = threading.Thread(target=printCount)
    t1.start()


def endThread():
    global killThread    
    while threading.activeCount() > 1:
        killThread = True
        print("Ending...")
    
    killThread = False
    print("Thread Stopped")
     

def printCount():
    global killThread
    count = 0
    while killThread == False:        
        print(count)
        count = count + 1
        time.sleep(5)


print("Thread Count: ", threading.activeCount())
startThread()
count = 0
while count < 11:
    print("Thread Count: ", threading.activeCount())
    time.sleep(1)
    count = count + 1
endThread()
#time.sleep(5)
print("Thread Count: ", threading.activeCount())
