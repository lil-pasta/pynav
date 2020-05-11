import curses
import os
from controller import name_box, ls_dir, get_dir, debug, info_box

#the application itself will be a userInterface object containing the rest of the application
class UserInterface:
    def __init__(self, stdscr, path):
        self.stdscr = stdscr
        self.path = [path, None, None]
        self.w = self.stdscr.getmaxyx()[1]
        self.pos = [1, 1, 1]
        self.sel = [1, 1, 1]
        self.focus = 0
        self.win1 = Box(self.stdscr, 1, 0)
        self.win2 = Box(self.stdscr, self.w//3 +1, 1)
        self.win3 = Box(self.stdscr, 2*self.w//3, 2)
        self.windows = [self.win1, self.win2, self.win3]

        #get curses movin'
        # -1 color value is the default used by curses
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        # border color
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.curs_set(0)
        self.stdscr.clear()
        self.stdscr.border(0)

    def draw(self, pos):
        self.stdscr.refresh()
        self.win1.draw()
        self.win2.draw()
        self.win3.draw()

    def get_key(self):
        ls_dir(self.windows[self.focus], self.path[0],
               self.sel[self.focus], self.pos[self.focus])
        name_box(self.windows[self.focus], self.path[0], self.focus)
        info_box(self.windows[2], self.path[0], self.sel[self.focus])
        while 1:
            key = self.stdscr.getch()
            if key == curses.KEY_UP and self.pos[self.focus] > 1:
                if self.pos[self.focus] == self.sel[self.focus]:
                    self.pos[self.focus] -= 1
                    self.sel[self.focus] -= 1
                    ls_dir(self.windows[self.focus], self.path[0],
                           self.sel[self.focus], self.pos[self.focus])
                    info_box(self.windows[2], self.path[0], self.sel[self.focus])
                else:
                    self.sel[self.focus] -= 1
                    ls_dir(self.windows[self.focus], self.path[0],
                           self.sel[self.focus], self.pos[self.focus])
                    info_box(self.windows[2], self.path[0], self.sel[self.focus])
            if key == curses.KEY_DOWN:
                if self.pos[self.focus] <= self.windows[self.focus].h - 3 \
                   and self.sel[self.focus] <= len(get_dir(self.path[0]))-1:
                    self.pos[self.focus] += 1
                    self.sel[self.focus] += 1
                    ls_dir(self.windows[self.focus], self.path[0],
                           self.sel[self.focus], self.pos[self.focus])
                    info_box(self.windows[2], self.path[0], self.sel[self.focus])
                else:
                    if self.sel[self.focus] <= len(get_dir(self.path[0]))-1:
                        self.sel[self.focus] += 1
                        ls_dir(self.windows[self.focus], self.path[0],
                               self.sel[self.focus], self.pos[self.focus])
                        info_box(self.windows[2], self.path[0], self.sel[self.focus])
            if key == curses.KEY_LEFT and self.focus > 0:
                self.focus -= 1
            if key == curses.KEY_RIGHT and self.focus < 1:
                self.focus += 1
            if key == ord('q'):
                exit()
            for window in self.windows[:2]:
                name_box(window, self.path[0], self.focus)

    #event loop goes here
    def run(self):
        self.draw(0)
        self.get_key()

class Box:
    def __init__(self, stdscr, start_w, box_num):
        self.stdscr = stdscr
        self.start_w = start_w
        self.number = box_num
        self.box = curses.newwin(self.stdscr.getmaxyx()[0]-2,
                                 self.stdscr.getmaxyx()[1]//3-2, 1,
                                 self.start_w)
        self.h, self.w = self.box.getmaxyx()
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
