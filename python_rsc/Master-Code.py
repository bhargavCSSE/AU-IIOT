# Author: Bhargav Joshi
# OCT 09, 2019
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

from guizero import *
from math import sqrt, exp
from time import sleep
from pathlib import Path
from curses import wrapper
from datetime import datetime
from threading import Thread, currentThread, RLock
from adafruit_ads1x15.analog_in import AnalogIn


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


def open_window():
    window.show()


def close_window():
    window.hide()
    t1.isAlive = False
    t2.isAlive = False
    sys.exit(e)


def calculate():
    Speed.value = round(
        (12/3.14159265*float(cutting_speed.value)/float(tool_size.value)), -1)
    Feed.value = round(
        (float(Speed.value)*float(chip_load.value)*float(flute_number.value)), 1)
    Sug_Speed.value = round(
        (12/3.14159265*float(cutting_speed.value)/float(tool_size.value)), -1)
    Sug_Feed.value = round(
        (float(Speed.value)*0.0018*float(flute_number.value)), 1)


def update_suggest(selected_value):
    if selected_value == "Aluminum":
        suggested_speed.value = "100-300 fpm"
    elif selected_value == "Brass & Bronze":
        suggested_speed.value = "80-200 fpm"
    elif selected_value == "Cast Iron":
        suggested_speed.value = "80-100 fpm"
    elif selected_value == "Steel - Free Machining":
        suggested_speed.value = "100-150 fpm"
    elif selected_value == "Steel - Low Carbon":
        suggested_speed.value = "80-100 fpm"
    elif selected_value == "Steel - Alloy":
        suggested_speed.value = "80-100 fpm"
    elif selected_value == "Steel - Tool":
        suggested_speed.value = "40-60 fpm"
    else:
        suggested_speed.value = "40-60 fpm"


def disp(stdscr):
    global rpm, adxl, current, timestamp, captured_samples
    rpm = 0

    # Clear screen
    stdscr.clear()


    while(True):
        stdscr.addstr(3, 10, '                                                          ')
        stdscr.addstr(5, 10, '                                                          ')
        stdscr.addstr(7, 10, '                                                          ')
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
        stdscr.addstr(13, 0, 'Time Elapsed:  {}'.format(round(timestamp,2)))
        stdscr.addstr(14, 0, 'Captured Samples: {}'.format(captured_samples))


        stdscr.clrtoeol()
        stdscr.refresh()


# Thread Definitions

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
    adxl = (0,0,0)
    current = 0
    
    start_time = time.time()
    captured_samples = 0
    while(True):
        date = datetime.now().strftime('%Y-%m-%d')
        Time = datetime.now().strftime('%H:%M:%S.%f')
        x,y,z = adxl
        timestamp = time.time() - start_time
        d.append({'Date': date, 'Time': Time,'Timestamp': timestamp, 'RPM': rpm, 'X': x,'Y': y,'Z': z, 'Current': current})
        df = pd.DataFrame(d)
        captured_samples += 1
        if t4.isAlive == False:
            print("DataFrame closing")
            print(df)
            filename = input("Filename? ")
            filename = filename+'.csv'
            df.to_csv(data_folder / filename)
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
        if(input("Turn on GUI? y/n: ") == 'y'):
            app = App(title='User Interface (Beta)',
            height=800,
            width=480,
            layout='grid')

            window = Window(app,title="Second Window",layout="grid")
            window.hide()

            title=Text(app,text="Select The Correct Values",align="left",grid=[1,0])

            tool_size=Combo(app,options=["0.125","0.25","0.375","0.5","0.625","0.75"],selected="0.5",grid=[1,1],align="left")
            tool_title=Text(app,"Mill Size",grid=[0,1],align="right")

            metal_type=Combo(app,options=["Aluminum","Brass & Bronze","Cast Iron","Steel - Free Machining","Steel - Low Carbon","Steel - Alloy", "Steel - Tool", "Stainless Steel"],grid=[1,2],align="left",command=update_suggest)
            metal_title=Text(app,"Metal Type",grid=[0,2],align="right")    

            suggested_speed=Text(app,text="100-300 fpm",grid=[1,3],align="left")
            suggested_title=Text(app,"Suggested FPM",grid=[0,3],align="right")

            cutter_material=ButtonGroup(app,options=["HSS","Carbide"],horizontal="yes", selected="HSS",grid=[1,4])
            cutter_title=Text(app,"Cutter Material",grid=[0,4],align="right")

            cutting_speed=Combo(app,options=["40","60","80","100","120","140","165","200","250","300"],selected="100",grid=[1,5],align="left")
            cutting_title=Text(app,"Cutting Speed (fpm)",grid=[0,5],align="right")

            flute_number=Combo(app,options=["2","3","4","5","6","8"],selected="2",grid=[1,6],align="left")
            flute_title=Text(app,"Cutting Edges",grid=[0,6],align="right")

            chip_load=Combo(app,options=["0.004","0.005","0.006","0.007","0.008","0.009","0.010"],selected="0.005",grid=[1,7],align="left")
            chip_title=Text(app,"Chip Load",grid=[0,7],align="right")

            calculate_button= PushButton(app, command = calculate,text="Calculate", grid=[1,9])

            Speed_title=Text(app, text = "RPM",grid=[0,10],align="right")
            Speed=Text(app,text="720",grid=[1,10],size=20,align="left")

            Feed_title=Text(app, text = "Feed",grid=[0,11],align="right")
            Feed=Text(app, text="7.6",grid=[1,11],size=20,align="left")

            Start_Program=PushButton(app,command = open_window,text="Record",grid=[1,13])

            #__________For second window things__________  


            Sug_Speed_title=Text(window,text="Suggested Speed",grid=[0,1],align="right")
            Sug_Speed=Text(window,text="760",grid=[1,1],align="right")
            Sug_Speed_Units=Text(window,text="RPM",grid=[2,1],align="left")

            Sug_Feed_title=Text(window,text="Suggested Feed Rate",grid=[0,2],align="right")
            Sug_Feed=Text(window,text="7.6",grid=[1,2],align="right")
            Sug_Speed_Units=Text(window,text="IPM",grid=[2,2],align="left")

            Tool_Speed_Title=Text(window,text="Tool Speed",grid=[0,3],align="right")
            Tool_Speed=Text(window," 0", grid=[1,3],align="right")
            Tool_Speed_Unit=Text(window,"RPM",grid=[2,3],align="left")

            X_Title=Text(window,text="X Magnitude",grid=[0,4],align="right")
            X=Text(window,text=" 0", grid=[1,4],align="right")
            X_Unit=Text(window,text="G",grid=[2,4],align="left")

            Y_Title=Text(window,text="Y Magnitude",grid=[0,5],align="right")
            Y=Text(window,text=" 0", grid=[1,5],align="right")
            Y_Unit=Text(window,text="G",grid=[2,5],align="left")

            Z_Title=Text(window,text="Z Magnitude",grid=[0,6],align="right")
            Z=Text(window,text=" 0", grid=[1,6],align="right")
            Z_Unit=Text(window,text="G",grid=[2,6],align="left")

            Current_Title=Text(window,text="Current Draw",grid=[0,7],align="right")
            Current=Text(window,text=" 0",grid=[1,7],align="right")
            Current_units=Text(window,text="Amps",grid=[2,7],align="left")

            Power_Title=Text(window,text="Power",grid=[0,8],align="right")
            Power=Text(window,text=" 0",grid=[1,8],align="right")
            Power_Units=Text(window,text="Watts",grid=[2,8],align="left") 

            

            Stop_Program=PushButton(window,command = close_window,text="Stop",grid=[2,9])
            Tool_Speed.after(1000, update_label)

            t1.start()
            t2.start()

            app.display()   

        else:
            t1.start()
            t2.start()
            if(input("Turn on terminal sensor display? y/n: ") == 'y'):
                wrapper(disp)
            else:
                while(True):
                    dummy_loop = 1
        

    except KeyboardInterrupt as e:
        t1.isAlive = False
        t2.isAlive = False
        sys.exit(e)
