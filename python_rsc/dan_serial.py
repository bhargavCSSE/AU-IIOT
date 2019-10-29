import serial
import time
ser=serial.Serial('/dev/ttyUSB0')
position=ser.readline().decode('utf-8').split(";")
length=len(position)
X,Y,Z,T,_=position[(length-5):]
X,Y,Z,T=X[:1],Y[1:],Z[1:],T[1:]
#xlist = [i for i in position if i.startswith("X")]
#ylist = [i for i in position if i.startswith("Y")]
#zlist = [i for i in position if i.startswith("Z")]
#tlist = [i for i in position if i.startswith("T")]
