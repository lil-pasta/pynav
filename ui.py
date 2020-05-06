import curses
import os

#the application itself will be a userInterface object containing the rest of the application
class UserInterface:
    def __init__(self, stdscr, path):
        self.stdscr = stdscr
        self.path = path
        self.w = self.stdscr.getmaxyx()[1]
        self.win1 = Box(self.stdscr, 1)
        self.win2 = Box(self.stdscr, self.w//3 +1)
        self.win3 = Box(self.stdscr, 2*self.w//3)

        #get curses movin'
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.border(0)

    def draw(self, pos):
        self.stdscr.refresh()
        self.win1.draw()
        self.win2.draw()
        self.win3.draw()

    def get_key(self):
        pos = 0
        while 1:
            key = self.stdscr.getch()
            if key == curses.KEY_UP and pos > 0:
                pos -= 1
            if key == curses.KEY_DOWN and pos < curses.LINES-5:
                pos += 1
            if key == ord('q'):
                exit()
            self.draw(pos)

    #event loop goes here
    def run(self):
        self.draw(0)
        self.get_key()

class Box:
    def __init__(self, stdscr, start_w):
        self.stdscr = stdscr
        self.start_w = start_w
        self.h, self.w = self.stdscr.getmaxyx()
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
