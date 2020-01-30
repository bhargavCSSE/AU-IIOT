# Author: Bhargav Joshi
# OCT 09, 2019
# Auburn Cyber Research Center (ACRC)
# Auburn, AL 36830

import threading
import time
import sys
import busio
import board
import RPi.GPIO as GPIO
import adafruit_adxl34x
import adafruit_ads1x15.ads1115 as ADS
import pandas as pd

from time import sleep
from threading import Thread, RLock
from adafruit_ads1x15.analog_in import AnalogIn

# Global Definitions


# Kernel
print("Loading kernel...")


# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# Kernel Setup
count = 0
loop_enable = 1
lock = RLock()


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.IN)


# Interrupt definitions
def interrupt_1(channel):
    global count
    count = count+1


# Interrupt deployments
GPIO.add_event_detect(11,GPIO.RISING,callback=interrupt_1)

# Thread definitions
def thread_RPM():
    global count
    while(loop_enable == 1):
        stamp1=count
        sleep(0.5)
        stamp2=count
        global ppm
        ppm = 60*(abs(stamp1 - stamp2))
        print("RPM: "+ str(ppm))

def thread_ADXL345():
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    while(loop_enable == 1):
        global adxl
        adxl = accelerometer.acceleration
        print("%f %f %f" % accelerometer.acceleration)
        sleep(1)

def thread_ADS1x15():
    ads = ADS.ADS1115(i2c)
    ads.gain = 4
    chan = AnalogIn(ads, ADS.P0, ADS.P1)
    while(loop_enable == 1):
        # x = []
        # for i in range(100):
        #     x.append(((chan.voltage**2)**.5)*60)
        #     sleep(0.01)
        # current = max(x)
        global current
        current = ((chan.voltage**2)**.5)*60
        print("Peak Current: " + str(current))
        sleep(0.1)

def thread_DataFrame(): 
    print("Initializing...")
    sleep(1)
    print("DataFrame in action")
    d = []
    global ppm, adxl, current
    for i in range(100):
        d.append({'RPM': ppm, 'ADXL': adxl, 'Current': current})
        df = pd.DataFrame(d)
        sleep(0.1)
    print(df)


# Kernel Execution
t1 = threading.Thread(name='RPM', target=thread_RPM, daemon=True)
t2 = threading.Thread(name='Accel', target=thread_ADXL345, daemon=True)
t3 = threading.Thread(name='ADS', target=thread_ADS1x15, daemon=True)
t4 = threading.Thread(name='DataFrame', target=thread_DataFrame)

t1.start()
t2.start()
t3.start()
t4.start()

print("started")
t4.join()
print("Finished")
