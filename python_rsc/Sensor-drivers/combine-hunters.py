import time
import board
import busio
import os
import csv
import adafruit_ads1x15.ads1115 as ADS
import adafruit_adxl34x
from adafruit_ads1x15.analog_in import AnalogIn
from os.path import expanduser
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mfrc522
from datetime import datetime


def setup():
    #Create the I2C Bus
    i2c = busio.I2C(board.SCL, board.SDA)

    #Create the ADC object using the I2C bus
    ads = ADS.ADS1115(i2c)
    accel = adafruit_adxl34x.ADXL345(i2c)

    #Create single-ended input on channel 0, 1, and 2
    chan = AnalogIn(ads, ADS.P0)
    chan1 = AnalogIn(ads, ADS.P1)
    chan2 = AnalogIn(ads, ADS.P2)
    #Create differential input between channel 0 and 1
    #chan = AnalogIn(ads, ADS.P0, ADS.P1)

    return (accel, chan, chan1, chan2)

# starts the program by making a RFID tag be swipped to activate the sensor code
def rfid_start():
    reader = SimpleMFRC522()
    while True:
        try:
            print('[*] Scan RFID card to begin session')
            id, text = reader.read()
            print('[*] Scanned --> RFID: {0}, Text: {1}'.format(id, text))
        finally:
            return (reader, id, text)

#
def collect_data(f, accel, chan, chan1, chan2):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S.%f')
    X, Y, Z = accel.acceleration
    vibration = ((X**2)+(Y**2)+(Z**2))**.5
    line = '{0},{1},{2},{3},{4},{5}\n'.format(timestamp, chan.value, chan.voltage, vibration, chan1.value, chan2.value)
    f.write(line)
    print(line)
    time.sleep(0.005)


# Any ID can turn on the system (may want to whitelist these eventually though)
# Valid IDs for turning off the system
valid_ids_to_stop = [246165292982]

def main():

    accel, chan, chan1, chan2  = setup()

    while True:
        reader, id, text = rfid_start()

        #file name will give the path and the name the file will be saved as
        file_name = '/home/pi/{0}.csv'.format(id)
        # check to see if file already exisits. If so, appends. If not, open new file and add headers
        if not os.path.exists(file_name):
            print("[*] File {0} doesn't exist! Creating and opening...\n".format(file_name))
            f = open(file_name, 'w')
            f.write("time,raw,v,vibration,raw1,raw2\n")
        else:
            print("[*] File {0} exists! Opening...\n".format(file_name))
            f = open(file_name, 'a')

        try:
            while True:
                if reader.read_id_no_block() in valid_ids_to_stop:
                    print('[*] Session ending')
                    raise Exception('[*] Session Ending')
                collect_data(f, accel, chan, chan1, chan2)
        except Exception:
            f.close()
            time.sleep(1)

if __name__ == '__main__':
    main()
