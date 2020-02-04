import threading
import sys
from time import sleep
from threading import RLock
import pandas as pd


lock = RLock()


def thread_1(name):
    global par1
    par1 = 1
    while(True):
        par1 += 1
        sleep(0.1)


def thread_2(name):
    global par2
    par2 = 1
    while(True):
        par2 += 1
        sleep(0.1)


def thread_3(name):
    global par3
    par3 = 1
    while(True):
        par3 += 1
        sleep(0.1)


def thread_4(name):
    d = []
    x4 = threading.currentThread()
    x4.isAlive = True
    global par1, par2, par3
    while(True):
        d.append({'par1': par1, 'par2': par2, 'par3': par3})
        df = pd.DataFrame(d)

        if not x4.isAlive:
            print("Exiting")
            print(df)
            break

        sleep(0.1)


if __name__ == "__main__":

    x1 = threading.Thread(target=thread_1, args=(1,), daemon=True)
    x2 = threading.Thread(target=thread_2, args=(1,), daemon=True)
    x3 = threading.Thread(target=thread_3, args=(1,), daemon=True)
    x4 = threading.Thread(target=thread_4, args=(1,))

    try:
        x1.start()
        x2.start()
        x3.start()
        x4.start()
        while(True):
            dummy_loop = 1
    
    except KeyboardInterrupt as e:
        x4.isAlive = False
        sys.exit(e)
