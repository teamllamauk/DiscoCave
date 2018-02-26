#!/usr/bin/env python3

import threading
import time

global killThread
killThread = False


def startThread():
    print("Start Thread")
    t1 = threading.Thread(target=playSound)
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



startThread()
time.sleep(20)
endThread()
