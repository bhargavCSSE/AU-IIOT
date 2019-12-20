import threading
from threading import Thread
import time
import sys
from time import sleep
import RPi.GPIO as GPIO

print("Loading kernel...")
count = 0
var1 = 1

GPIO.setmode(GPIO.BCM)
GPIO.setup(11,GPIO.IN)

def interrupt_1(channel):
    global count
    count = count+1
    print(count)

GPIO.add_event_detect(11,GPIO.RISING,callback=interrupt_1)

def counter():
    while(var1 == 1):
        stamp1=count
        sleep(60)
        stamp2=count
        global ppm
        ppm = (abs(stamp1 - stamp2))
        # count = 0
        print("Pulse per min: "+ str(ppm))

def thread_2():
    loop = 1
    while(var1 == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1)

w2 = threading.Thread(name='counter', target=counter)

w2.start()

print("started")

