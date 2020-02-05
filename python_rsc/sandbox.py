# from curses import wrapper

import curses
from curses import wrapper
from time import sleep

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 11):
        v = i-10
        stdscr.addstr(1, 0, '10 divided by {} is {}'.format(v, 10/v))
        stdscr.addstr(2, 0, '20 divided by {} is {}'.format(v, 20/v))
        stdscr.refresh()
        stdscr.clear()
        sleep(0.5)

    stdscr.getkey()


wrapper(main)
