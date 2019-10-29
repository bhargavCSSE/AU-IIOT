import serial
import time
ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,timeout=15)
#time.sleep(5)
while True:
        try:
                position=ser.readline().decode(encoding='utf-8',errors='ignore').split(";")
                X=Y=Z=T=""
                if len(position)<5:
                        pass
                elif len(position) == 5:
                        X,Y,Z,T,_=position
                else:
                        X,Y,Z,T,_=position[(len(position)-5):]
                line='{0},{1},{2},{3}'.format(X,Y,Z,T)
                print(line)
        except:
                raise
