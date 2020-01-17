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

GPIO.add_event_detect(11,GPIO.RISING,callback=interrupt_1)

def thread_counter():
    while(var1 == 1):
        stamp1=count
        sleep(1)
        stamp2=count
        global ppm
        ppm = 60*(abs(stamp1 - stamp2))
        # count = 0
        print("Pulse per min: "+ str(ppm)) 

def thread_2():
    loop = 1
    while(var1 == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1/10)

def thread_3():
    loop = 1
    while(var1 == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1/100)

def thread_4():
    loop = 1
    while(var1 == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1/1000)

t1 = threading.Thread(name='counter', target=thread_counter)
t2 = threading.Thread(name='thread-2', target=thread_2)
t3 = threading.Thread(name='thread-2', target=thread_3)
t4 = threading.Thread(name='thread-2', target=thread_4)

t1.start()
t2.start()
t3.start()
t4.start()

print("started")


# grey: Digital
# Purple: Ground
# Blue: Voltage