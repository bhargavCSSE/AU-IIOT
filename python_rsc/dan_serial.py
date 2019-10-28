import serial
import time
ser=serial.Serial('/dev/ttyUSB0')
position=ser.read(100).decode('utf-8').split(";")
xlist = [i for i in position if i.startswith("X")]
ylist = [i for i in position if i.startswith("Y")]
zlist = [i for i in position if i.startswith("Z")]
tlist = [i for i in position if i.startswith("T")]
