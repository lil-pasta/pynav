import curses, os

def debug(function, message):
    debug_file = os.curdir + '/debug.txt'
    with open(debug_file, 'a') as f:
        f.write(f"Output from {function} : {message}")

def get_dir(path):
    return [f for f in os.listdir(path)]

def name_box(box, path, focus):
    if focus == box.number:
        box.box.wattron(curses.color_pair(2))
        box.box.addstr(0, 4, path, curses.color_pair(1))
        debug(name_box.__name__, path)
    else:
        box.box.addstr(0, 2, path, curses.A_NORMAL)
        debug(name_box.__name__, path)
    box.box.refresh()

def ls_dir(box, path, pos):
    h, w = box.box.getmaxyx()
    items = get_dir(path)
    for index in range(0, h-4):
        if index <= len(items)-1:
            if index == pos:
                box.box.addstr(index+1, 2, items[index], curses.color_pair(1))
            else:
                box.box.addstr(index+1, 2, items[index], curses.A_NORMAL)
    box.stdscr.refresh()
    box.box.refresh()


# def process_enter():
