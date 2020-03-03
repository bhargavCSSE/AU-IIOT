# Author: Bhargav Joshi & Daniel Abernathy 
# FEB 27, 2020
# Auburn Cyber Research Center (ACRC)
# Auburn, AL 36830

import threading
import random
import time
import sys
import busio
import board
import RPi.GPIO as GPIO
import adafruit_adxl34x
import adafruit_ads1x15.ads1115 as ADS
import pandas as pd


from math import sqrt, exp
from time import sleep
from pathlib import Path
from curses import wrapper
from datetime import datetime
from threading import Thread, currentThread, RLock
from adafruit_ads1x15.analog_in import AnalogIn
from mfrc522 import SimpleMFRC522


# Function Definitions

def read_sensor():
    global rpm, adxl, current
    X1_Speed = round(rpm, 5)
    X2_X, X2_Y, X2_Z = adxl
    X3_Current = round(current,5)
    return [X1_Speed, X2_X, X2_Y, X2_Z, X3_Current]

def update_label():
    reading = read_sensor()
    Tool_Speed.value = reading[0]
    X.value = round(reading[1], 8)
    Y.value = round(reading[2], 8)
    Z.value = round(reading[3], 8)
    Current.value = round(reading[4], 8)
    Power_Value = sqrt(pow(float(reading[2]), 2))*120
    Power.value = round(Power_Value,5)
    # recursive call
    Tool_Speed.after(1000, update_label)





def disp(stdscr):
    global rpm, adxl, current, timestamp, captured_samples
    rpm = 0

    # Clear screen
    stdscr.clear()


    while(True):
        stdscr.addstr(3, 10, '                                                          ')
        stdscr.addstr(6, 10, '                                                          ')
        stdscr.addstr(7, 10, '                                                          ')
        stdscr.addstr(8, 10, '                                                          ')
        stdscr.addstr(10, 10, '                                                          ')
        stdscr.addstr(0, 0, "Sensor-Display (Beta testing)")
        stdscr.addstr(1, 0, '-----------------------------------------------------------')
        stdscr.addstr(3, 0, 'RPM:')
        stdscr.addstr(3, 10, '{}'.format(rpm))
        stdscr.addstr(5, 0, 'ADXL:')
        stdscr.addstr(6, 1, 'X:')
        stdscr.addstr(6, 10, '{}'.format(adxl[0]))
        stdscr.addstr(7, 1, 'Y:')
        stdscr.addstr(7, 10, '{}'.format(adxl[1]))
        stdscr.addstr(8, 1, 'Z:')
        stdscr.addstr(8, 10, '{}'.format(adxl[2]))
        stdscr.addstr(10, 0, 'Current:')
        stdscr.addstr(10, 10, '{}'.format(current))
        stdscr.addstr(12, 0, '-----------------------------------------------------------')
        
        stdscr.clrtoeol()
        stdscr.refresh()


# Thread Definitions
def thread_RFID():
    print("Initializing thread: RFID")
    t6 = currentThread()
    t6.isAlive = True
    reader = SimpleMFRC522()
    while(loop_enable == 1):
        global RF_ID
        global RF_text
        RF_ID, RF_text = reader.read()
        print(RF_ID, RF_text)
        if t6.isAlive == False:
            print("RFID closing")
            break

def thread_I2C():
    print("Initializing thread: I2C")
    t2 = currentThread()
    t2.isAlive = True
    accelerometer = adafruit_adxl34x.ADXL345(i2c)
    ads = ADS.ADS1115(i2c)
    ads.gain = 4
    chan = AnalogIn(ads, ADS.P0, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    chan3 = AnalogIn(ads, ADS.P3)
    
    while(loop_enable == 1):
        global adxl
        adxl = accelerometer.acceleration
        global current
        current = ((chan.voltage**2)**.5)*60
        global sound
        sound = chan2.voltage
        global sound2
        sound2 = chan3.voltage
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
    global rpm, adxl, current, timestamp, captured_samples, sound, sound2, RF_ID, RF_text
    rpm = 0
    adxl = (0,0,0)
    current = 0
    sound = 0
    sound2 = 0
    RF_ID = 0
    RF_text = 0
    
    start_time = time.time()
    captured_samples = 0
    while(True):
        date = datetime.now().strftime('%Y-%m-%d')
        Time = datetime.now().strftime('%H:%M:%S.%f')
        x,y,z = adxl
        timestamp = time.time() - start_time
        d.append({'Date': date, 'Time': Time,'Timestamp': timestamp, 'RPM': rpm, 'X': x,'Y': y,'Z': z, 'Current': current, 'Sound':sound,'Sound2':sound2,"RFID":RF_ID,"RFID_Text":RF_text})
        df = pd.DataFrame(d)
        captured_samples += 1
        if t4.isAlive == False:
            print("DataFrame closing")
            print(df)
            filename = input("Filename? ")
            df.to_csv(data_folder / filename)
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
    GPIO.setup(27, GPIO.IN)

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
    GPIO.add_event_detect(27, GPIO.RISING, callback=interrupt_1)

    # Kernel Execution
    t1 = threading.Thread(name='I2C', target=thread_I2C, daemon=True)
    t2 = threading.Thread(name='DataFrame', target=thread_DataFrame)
    t6 = threading.Thread(name='RFID', target=thread_RFID)

    try:
        t1.start()
        t2.start()
        t6.start()        
        # wrapper(disp)
        

    except KeyboardInterrupt as e:
        t1.isAlive = False
        t2.isAlive = False
        t6.isAlive = False
        sys.exit(e)