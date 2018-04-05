#!/usr/bin/env python3

# Imports
import time
import datetime


timeNow = datetime.datetime.now().time()
print(timeNow)

utc_dt = datetime.datetime.now(datetime.timezone.utc)
print(utc_dt)

dt = utc_dt.astimezone()
print(dt)
