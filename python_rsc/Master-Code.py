import threading
from threading import Thread
import time
import sys
from time import sleep
import RPi.GPIO as GPIO
import adafruit_adxl34x

# Global Definitions


# Kernel
print("Loading kernel...")


# Kernel Setup
count = 0
loop_enable = 1


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
        sleep(1)
        stamp2=count
        global ppm
        ppm = 60*(abs(stamp1 - stamp2))
        print("RPM: "+ str(ppm))

def thread_2():
    loop = 1
    while(loop_enable == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1)

def thread_3():
    loop = 1
    while(loop_enable == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1)

def thread_4():
    loop = 1
    while(loop_enable == 1):
        print("Interrupt-1 loop count= "+str(loop))
        loop = loop+1
        sleep(1)


# Kernel Execution
t1 = threading.Thread(name='RPM', target=thread_RPM)
t2 = threading.Thread(name='thread-2', target=thread_2)
#t3 = threading.Thread(name='thread-2', target=thread_3)
#t4 = threading.Thread(name='thread-2', target=thread_4)

t1.start()
t2.start()
#t3.start()
#t4.start()

print("started")
