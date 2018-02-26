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
    killThread = True
    print("End Thread")
     

def printCount():
    global killThread
    count = 0
    while killThread == False:        
        print(count)
        count = count + 1


print("Thread Count: ", threading.activeCount())
startThread()
count = 0
while count < 11:
    print("Thread Count: ", threading.activeCount())
    time.sleep(1)
    count = count + 1
endThread()
print("Thread Count: ", threading.activeCount())
