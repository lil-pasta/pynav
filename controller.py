import curses, os

def debug(function, message):
    debug_file ='/home/sh/Dev/pynav/debug.txt'
    with open(debug_file, 'a') as f:
        f.write(f"Output from {function} : {message} \n")

def get_dir(path):
    return [('d', f) if os.path.isdir(f) else ('f', f) \
            for f in sorted(os.listdir(path), key=lambda x: x.lower())]

def name_box(box, path, focus):
    if focus == box.number:
        box.box.attron(curses.color_pair(3))
        box.box.border(0)
        box.box.addstr(0, 2, path, curses.color_pair(1))
        box.box.attroff(curses.color_pair(3))
    else:
        box.box.border(0)
        box.box.addstr(0, 2, path, curses.A_NORMAL)
    box.box.refresh()

def scrolling(box, sel, items):
    b_h = box.h - 2
    num_items = len(items)
    if b_h >= num_items:
        return (0, b_h)
    if b_h < num_items and sel <= b_h:
        return (0, b_h)
    if b_h < num_items and sel > b_h:
        if sel <= num_items:
            new_start = sel - b_h
            new_finish = sel
            return (new_start, new_finish)
        else:
            return scrolling(box, sel-1, items)

def ls_dir(box, path, sel, pos):
    h, w = box.h, box.w
    items = get_dir(path)
    clear_str = ' '*(w)
    scroll = scrolling(box, sel, items)
    debug(ls_dir.__name__, f"{scroll}, {pos}, {sel}")
    for index, item in enumerate(items[scroll[0]:scroll[1]]):
        index += 1
        debug('index, item', f"{index}, {item}")
        box.box.addstr(index, 2, clear_str)
        if index == pos and item[0] == 'd':
            d_name = item[1] + '/'
            box.box.addstr(index, 2, d_name, curses.color_pair(1) | curses.A_BOLD)
        if index == pos and item[0] != 'd':
            box.box.addstr(index, 2, item[1], curses.color_pair(1))
        if index != pos and item[0] == 'd':
            # we have to delete the slash we added when the dir was highlighted lol
            box.box.addstr(index, 2, item[1]+' ', curses.A_NORMAL | curses.A_BOLD)
        if index != pos and item[0] != 'd':
            box.box.addstr(index, 2, item[1], curses.A_NORMAL)
    box.stdscr.refresh()
    box.box.refresh()

#def info_box(box, items):



# def process_enter():
