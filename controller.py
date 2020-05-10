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
    for index, item in enumerate(items[scroll[0]:scroll[1]]):
        index += 1
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


def permission_string(item):
    """builds one of those easily readable strings from the permissions byte code"""
    stats = os.stat(item[1])
    perms = oct(stats.st_mode)[-3:]
    if item[0] == 'd':
        perm_string = 'd'
    else:
        perm_string = '-'
    for number in perms:
        if number == '0':
            perm_string = perm_string + '---'
        if number == '1':
            perm_string = perm_string + '--x'
        if number == '2':
            perm_string = perm_string + '-w-'
        if number == '3':
            perm_string = perm_string + '-wx'
        if number == '4':
            perm_string = perm_string + 'r--'
        if number == '5':
            perm_string = perm_string + 'r-x'
        if number == '6':
            perm_string = perm_string + 'rw-'
        if number == '7':
            perm_string = perm_string + 'rwx'
    return perm_string

def info_box(box, path, sel):
    """prints some info on the current highlighted file"""
    """file name, file size, file type, permissions"""
    h, w = box.h, box.w
    clear_str = ' '*int(w-2)
    file_info = {}
    item = get_dir(path)[sel-1]
    file_info['file_name'] = item[1]
    try:
        file_info['file_size'] = str(os.path.getsize(item[1])/1000) + 'kb'
    except os.error as error:
        file_info['file_size'] = error
    file_info['file_type'] = os.path.splitext(item[1])[1]
    file_info['permissions'] = permission_string(item)

    for index, item in enumerate(file_info.values()):
        y = int(h/2 - len(file_info) + index)
        x = int(w/2-len(item)/2)
        box.box.addstr(y, 1, clear_str)
        box.box.addstr(y, x, item, curses.A_NORMAL)
    box.box.refresh()




# def process_enter():
