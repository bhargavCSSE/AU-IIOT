# Serial Port Reader
# Author: Bhargav Joshi
# OCT 09, 2019
# Auburn Cyber Research Center (ACRC)
# Auburn, AL 36830

import serial
import pandas as pd
from datetime import datetime

SERIAL_PORT = '/dev/cu.usbserial-AK06QCKG'
BAUD_RATE = 9600
BYTE_BUFFER_SIZE = 8

ser_instance_1 = serial.Serial(
        
        port=SERIAL_PORT,
        baudrate = BAUD_RATE,
        timeout = 1
        
        )
#Exit program using  keyboard interrupt (Ctrl + C)
df = pd.DataFrame(columns=["Date","Time","Current", "RPM"])
index = 0
try:
    while 1:
        # serial_input = ser_instance_1.read(BYTE_BUFFER_SIZE)
        serial_input = str(ser_instance_1.readline()).replace("\\r\\n'","")
        serial_input = serial_input.split(',')
        df = df.append(dict(Date=datetime.now().strftime('%Y-%m-%d'),
                            Time=datetime.now().strftime('%H:%M:%S.%f'),
                            Current=serial_input[1:2],
                            RPM=serial_input[3:4]), ignore_index=True)
        print(str(serial_input))
except KeyboardInterrupt:
    print("\nKeyboard Interrupt Detected...Closing serial read")
    print(df)
    df.to_csv("current-rpm.csv")