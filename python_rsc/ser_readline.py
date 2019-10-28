import serial
import time
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=1)
time.sleep(1)
while True:
        try:
                position=ser.readline().decode('utf-8')
                #     position=ser.readline().decode('utf-8').split(";")
                #     xlist=[i for i in position if i.startswith("X")]
                #     ylist=[i for i in position if i.startswith("Y")]
                #     zlist=[i for i in position if i.startswith("Z")]
                #     tlist=[i for i in position if i.startswith("T")]
                #     print(xlist)
                print(position)
        #       print(position[0])
                if position[0] =="X":
                        X, Y, Z, b = position.split(";")
                elif position[0] == "T":
                        T, b = position.split(";")
                else:
                        pass
        #               ser.flush()
                time.sleep(1)
        except:
                raise







