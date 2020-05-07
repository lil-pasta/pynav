import curses
import os
from controller import name_box, ls_dir, get_dir

#the application itself will be a userInterface object containing the rest of the application
class UserInterface:
    def __init__(self, stdscr, path):
        self.stdscr = stdscr
        self.path = [path, None, None]
        self.w = self.stdscr.getmaxyx()[1]
        self.pos = [0, 0, 0]
        self.focus = 0
        self.win1 = Box(self.stdscr, 1, 1)
        self.win2 = Box(self.stdscr, self.w//3 +1, 2)
        self.win3 = Box(self.stdscr, 2*self.w//3, 3)
        self.windows = [self.win1, self.win2, self.win3]

        #get curses movin'
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_WHITE)
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.border(0)

    def draw(self, pos):
        self.stdscr.refresh()
        self.win1.draw()
        self.win2.draw()
        self.win3.draw()

    def get_key(self):
        ls_dir(self.windows[self.focus], self.path[0], self.pos[self.focus])
        name_box(self.windows[self.focus], self.path[0], self.focus)
        while 1:
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.pos[self.focus] > 0:
                self.pos[self.focus] -= 1
            if key == curses.KEY_DOWN and self.pos[self.focus] < len(get_dir(self.path[0]))-1:
                self.pos[self.focus] += 1
            if key == curses.KEY_LEFT and self.focus > 0:
                self.focus -= 1
            if key == curses.KEY_RIGHT and self.focus < 2:
                self.focus += 1
            if key == ord('q'):
                exit()
            ls_dir(self.windows[self.focus], self.path[0], self.pos[self.focus])
            name_box(self.windows[self.focus], self.path[0], self.focus)

    #event loop goes here
    def run(self):
        self.draw(0)
        self.get_key()

class Box:
    def __init__(self, stdscr, start_w, box_num):
        self.stdscr = stdscr
        self.start_w = start_w
        self.h, self.w = self.stdscr.getmaxyx()
        self.number = box_num
        self.box = curses.newwin(self.h-2, self.w//3-2, 1, self.start_w)
        self.box.box()
        self.box.border(0)

    def draw(self):
        self.box.refresh()

#this starts the application
def start_app(stdscr, path):
    app = UserInterface(stdscr, path)
    app.run()


def launch_pynav(curdir):
    curses.wrapper(start_app, curdir)
