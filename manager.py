import os, sys, curses
from curses import textpad
import time

# eventually we should add caching of visited directories so we can navigate back and forth between directories


# helpers/repeated
def get_screen(stdscr):
    h, w = stdscr.getmaxyx()
    return (h, w)

#pass os.curdir into this function so we can cache it later (memoization, decorator)
def get_items(curdir):
    return [f for f in os.listdir(curdir)]

def draw_box(stdscr):
    h, w = get_screen(stdscr)
    box = curses.newwin(h-2, w//3-2, 1, 1)
    box.box()
    box.border(0)
    return box

def ls_box(stdscr, box, curdir, pos):
    items = sorted(get_items(curdir))
    h, w = get_screen(stdscr)
    for index in range(0, h-4):
        if index == pos:
            box.addstr(index+1, 2, items[index], curses.color_pair(1))
        else:
            box.addstr(index+1, 2, items[index], curses.A_NORMAL)
    stdscr.refresh()
    box.refresh()

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.curs_set(0)
    pos = 0
    stdscr.clear()
    stdscr.border(0)
    os.chdir('/home/sh')
    box1 = draw_box(stdscr)
    ls_box(stdscr, box1, os.curdir, pos)
    while 1:
        key = stdscr.getch()
        if key == curses.KEY_UP and pos > 0:
            pos -= 1
        if key == curses.KEY_DOWN and pos < curses.LINES-5:
            pos += 1
        ls_box(stdscr, box1, os.curdir, pos)

if __name__ == "__main__":
    curses.wrapper(main)
