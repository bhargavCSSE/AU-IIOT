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
from pathlib import Path
from curses import wrapper
from datetime import datetime
from threading import Thread, currentThread, RLock
from adafruit_ads1x15.analog_in import AnalogIn


def display(stdscr):
    global rpm, adxl, current, timestamp, captured_samples
    rpm = 0
    # Clear screen
    stdscr.clear()


    while(True):
        stdscr.addstr(0, 0, "Sensor-Display (Beta testing)")
        stdscr.addstr(1, 0, "---------------------------------------------------------")
        stdscr.addstr(3, 0, 'RPM:')
        stdscr.addstr(3, 10, '{}'.format(rpm))
        stdscr.addstr(5, 0, 'ADXL:')
        stdscr.addstr(5, 10, '{}'.format(adxl))
        stdscr.addstr(7, 0, 'Current:')
        stdscr.addstr(7, 10, '{}'.format(current))
        stdscr.addstr(9, 0, '---------------------------------------------------------')
        stdscr.addstr(11, 0, 'Time Elapsed:  {}'.format(round(timestamp,2)))
        stdscr.addstr(12, 0, 'Captured Samples: {}'.format(captured_samples))
        stdscr.refresh()


def thread_I2C():
    print("Initializing thread: I2C")
    t2 = currentThread()
    t2.isAlive = True
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    ads = ADS.ADS1115(i2c)
    ads.gain = 4
    chan = AnalogIn(ads, ADS.P0, ADS.P1)
    
    while(loop_enable == 1):
        global adxl
        adxl = accelerometer.acceleration
        global current
        current = ((chan.voltage**2)**.5)*60
        # print("%f %f %f" % accelerometer.acceleration)
        
        if t2.isAlive == False:
            print("I2C closing")
            break

def thread_DataFrame(): 
    print("Initializing thread: DataFrame")
    t4 = currentThread()
    t4.isAlive = True

    data_folder = Path("Data")
    d = []
    global rpm, adxl, current, timestamp, captured_samples
    rpm = 0
    adxl = 0
    current = 0
    
    start_time = time.time()
    captured_samples = 0
    while(True):
        date = datetime.now().strftime('%Y-%m-%d')
        Time = datetime.now().strftime('%H:%M:%S.%f')
        timestamp = time.time() - start_time
        d.append({'Date': date, 'Time': Time,'Timestamp': timestamp, 'RPM': rpm, 'ADXL': adxl, 'Current': current})
        df = pd.DataFrame(d)
        captured_samples += 1
        if t4.isAlive == False:
            print("DataFrame closing")
            print(df)
            df.to_csv(data_folder / 'samples.csv')
            print("\nTotal Time of data collection:"+str(timestamp))
            break

if __name__ == "__main__":
    
    # Kernel
    print("Loading kernel...")

    # I2C setup
    i2c = busio.I2C(board.SCL, board.SDA)

    # Kernel Setup
    global count
    count = 0
    start_time = 0
    loop_enable = 1
    lock = RLock()

    # GPIO setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(11, GPIO.IN)

    # Interrupt definitions
    def interrupt_1(channel):
        global start_time
        global rpm
        if(start_time == 0):
            start_time = time.time()
        else:
            current_time = time.time()
            rpm = 60/(current_time - start_time)
            start_time = current_time


    # Interrupt deployments
    GPIO.add_event_detect(11, GPIO.RISING, callback=interrupt_1)

    # Kernel Execution
    t1 = threading.Thread(name='I2C', target=thread_I2C, daemon=True)
    t2 = threading.Thread(name='DataFrame', target=thread_DataFrame)

    try:
        t1.start()
        t2.start()
        if(input("Turn on sensor display? Y/N: ") == 'Y'):
            wrapper(display)
        else:
            while(True):
                dummy_loop = 1

    except KeyboardInterrupt as e:
        t1.isAlive = False
        t2.isAlive = False
        sys.exit(e)
        
