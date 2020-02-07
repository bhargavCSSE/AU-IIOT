#!/usr/bin/env python
from guizero import *
import random
from math import sqrt, exp


def read_sensor():
    X1_Speed = random.randrange(3200,5310,10)/100
    X2_Vibe =  random.randrange(1000,3000,10)/100
    X3_Current = random.randrange(100,700,10)/100
    return [X1_Speed,X2_Vibe,X3_Current]

def update_label():
    reading = read_sensor()
    Tool_Speed.value = reading[0]
    Vibration.value = reading[1]
    Current.value = reading[2]
    Power_Value=sqrt(pow(float(reading[2]),2))*120
    Power.value = Power_Value    
    # recursive call
    Tool_Speed.after(1000, update_label)

def open_window():
    window.show()

def close_window():
    window.hide()

def calculate():
    Speed.value =round((12/3.14159265*float(cutting_speed.value)/float(tool_size.value)),-1)
    Feed.value =round((float(Speed.value)*float(chip_load.value)*float(flute_number.value)),1)
    Sug_Speed.value =round((12/3.14159265*float(cutting_speed.value)/float(tool_size.value)),-1)
    Sug_Feed.value =round((float(Speed.value)*0.0018*float(flute_number.value)),1)


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

if __name__ == '__main__':
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

    Tool_Speed_Title=Text(window,text="Tool Speed",grid=[0,4],align="right")
    Tool_Speed=Text(window," 0", grid=[1,4],align="right")
    Tool_Speed_Unit=Text(window,"RPM",grid=[2,4],align="left")

    Vibration_Title=Text(window,text="Vibration Magnitude",grid=[0,5],align="right")
    Vibration=Text(window,text=" 0", grid=[1,5],align="right")
    Vibration_Unit=Text(window,text="G",grid=[2,5],align="left")

    Current_Title=Text(window,text="Current Draw",grid=[0,6],align="right")
    Current=Text(window,text=" 0",grid=[1,6],align="right")
    Current_units=Text(window,text="Amps",grid=[2,6],align="left")

    Power_Title=Text(window,text="Power",grid=[0,7],align="right")
    Power=Text(window,text=" 0",grid=[1,7],align="right")
    Power_Units=Text(window,text="Watts",grid=[2,7],align="left") 

    

    Stop_Program=PushButton(window,command = close_window,text="Stop",grid=[2,8])
  

    Tool_Speed.after(1000, update_label)

    app.display()
