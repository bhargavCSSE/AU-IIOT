import time
import board
import busio
import os
import serial
import redis
import csv
import adafruit_ads1x15.ads1115 as ADS
import adafruit_adxl34x
from adafruit_ads1x15.analog_in import AnalogIn
from os.path import expanduser
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mfrc522
from datetime import datetime




    #Create the I2C Bus
i2c = busio.I2C(board.SCL, board.SDA)

    #Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
accel = adafruit_adxl34x.ADXL345(i2c)

    #Create single-ended input on channel 0, 1, and 2
chan = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
#Create differential input between channel 0 and 1
    #chan = AnalogIn(ads, ADS.P0, ADS.P1)

    #Create the connection to the Redis Port
r = redis.Redis(host='localhost',port = '6379', decode_responses=True, db=0)

    #Create the serial port
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=1)
Xp = ''
Yp = ''
Zp = ''
Tp = ''

for loop in range(0,50):

        timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
        X, Y, Z = accel.acceleration
        vibration = ((X**2)+(Y**2)+(Z**2))**.5
        basedata = r.get("basedata")
        power1, power2, p1pp2, vrms,_,_,_,_,_,_,_ = [float(i) for i in basedata.$
        line = '{0},{1},{2},{3},{4},{5},{6},{7}'.format(timestamp, chan.value, c$
        print("line")
        print(line)
        try:
                position=ser.readline().decode('utf-8')
                if position[0] == "X":
                        Xp, Yp, Zp, b = position.split(";")
                elif position[0] == "T":
                        Tp, b = position.split(";")
                else:
                        pass
        except:
                pass
        print("position")
        pline = '{0},{1},{2},{3}'.format(Xp[1:],Yp[1:],Zp[1:],Tp[1:])
        print(pline)
        saveline=line+pline
