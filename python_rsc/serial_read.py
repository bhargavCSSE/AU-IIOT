# Serial Port Reader
# Author: Bhargav Joshi
# OCT 09, 2019
# Auburn Cyber Research Center (ACRC)
# Auburn, AL 36830

import serial
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
BYTE_BUFFER_SIZE = 8

ser_instance_1 = serial.Serial(
        
        port=SERIAL_PORT,
        baudrate = BAUD_RATE,
        timeout = 1
        
        )

#Exit program using  keyboard interrupt (Ctrl + C)

try:
    while 1:
        serial_input = ser_instance_1.read(BYTE_BUFFER_SIZE)
        print(str(serial_input))
except KeyboardInterrupt:
    print("\nKeyboard Interrupt Detected...Closing serial read")
