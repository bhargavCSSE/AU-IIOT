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
from curses import wrapper
from datetime import datetime
from threading import Thread, currentThread, RLock
from adafruit_ads1x15.analog_in import AnalogIn


def display(stdscr, pid):
    global ppm, adxl, current
    ppm = 0
    adxl = 0
    current = 0
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    while(True):
        stdscr.addstr(1, 0, 'RPM: {}'.format(ppm))
        stdscr.addstr(2, 0, 'ADXL: {}'.format(adxl))
        stdscr.addstr(3, 0, 'Current: {}'.format(current))
        stdscr.clear()
        if pid.isAlive == False:
            break
    stdscr.getkey()

# Thread definitions
def thread_RPM():
    print("Initializing thread: RPM")
    t1 = currentThread()
    t1.isAlive = True
    global count

    while(loop_enable == 1):
        stamp1=count
        sleep(0.1)
        stamp2=count
        global ppm
        ppm = 60*(abs(stamp1 - stamp2))
        # print("RPM: "+ str(ppm))
        
        if t1.isAlive == False:
            print("RPM closing")
            break


def thread_ADXL345():
    print("Initializing thread: ADXL")
    t2 = currentThread()
    t2.isAlive = True
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    
    while(loop_enable == 1):
        global adxl
        adxl = accelerometer.acceleration
        # print("%f %f %f" % accelerometer.acceleration)
        
        if t2.isAlive == False:
            print("ADXL closing")
            break


def thread_ADS1x15():
    t3 = currentThread()
    t3.isAlive = True
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
        # print("Peak Current: " + str(current))
        if t3.isAlive == False:
            print("ADS closing")
            break


def thread_DataFrame(): 
    print("Initializing thread: DataFrame")
    t4 = currentThread()
    t4.isAlive = True
    print("DataFrame in action")
    d = []
    global ppm, adxl, current
    ppm = 0
    adxl = 0
    current = 0
    
    while(True):
        date = datetime.now().strftime('%Y-%m-%d')
        time = datetime.now().strftime('%H:%M:%S.%f')
        d.append({'Date': date, 'Time': time, 'RPM': ppm, 'ADXL': adxl, 'Current': current})
        df = pd.DataFrame(d)
        if t4.isAlive == False:
            print("DataFrame closing")
            print(df)
            break
        sleep(0.1)

def thread_display():
    print("Initializing thread: Display")
    t5 = currentThread()
    t5.isAlive = True
    wrapper(display, t5)

if __name__ == "__main__":
    
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
    GPIO.setup(11, GPIO.IN)

    # Interrupt definitions
    def interrupt_1(channel):
        global count
        count = count+1

    # Interrupt deployments
    GPIO.add_event_detect(11, GPIO.RISING, callback=interrupt_1)

    # Kernel Execution
    t1 = threading.Thread(name='RPM', target=thread_RPM, daemon=True)
    t2 = threading.Thread(name='Accel', target=thread_ADXL345, daemon=True)
    t3 = threading.Thread(name='ADS', target=thread_ADS1x15, daemon=True)
    t4 = threading.Thread(name='DataFrame', target=thread_DataFrame)
    # t5 = threading.Thread(name='Display', target=thread_display)

    try:
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        # t5.start()
        while(True):
            dummy_loop = 1

    except KeyboardInterrupt as e:
        t1.isAlive = False
        t2.isAlive = False
        t3.isAlive = False
        t4.isAlive = False
        # t5.isAlive = False
        sys.exit(e)
