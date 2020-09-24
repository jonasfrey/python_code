import curses
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT
 
HEIGHT = 30
WIDTH = 50
X_MAX = HEIGHT - 2
Y_MAX = WIDTH - 2
 
def main(stdscr):
    window = curses.newwin(HEIGHT, WIDTH, 0, 0)
    window.keypad(1)
    curses.curs_set(0)
    window.border(0)
    window.timeout(1000)
 
    key_default = KEY_DOWN
    key_conflict_dict = {KEY_DOWN:KEY_UP, KEY_UP:KEY_DOWN,
                         KEY_LEFT:KEY_RIGHT, KEY_RIGHT:KEY_LEFT}
 
    rx = 2; ry = 23; #initial position
    window.addstr(rx, ry, '*')
 
 
 
    while True:
        window.refresh()
        ch = window.getch()
        if ch == 27:
            break
        elif ch in (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT):
            if key_conflict_dict[ch] != key_default:
                key_default = ch
 
        if key_default == KEY_DOWN:
            rx += 1
        elif key_default == KEY_UP:
            rx -= 1
        elif key_default == KEY_LEFT:
            ry -= 1
        elif key_default == KEY_RIGHT:
            ry += 1
 
        if rx > X_MAX: rx = X_MAX
        if ry < 1: ry = 1
 
 
        window.clear()
        window.border(0)
        window.addstr(rx, ry, '*')
 
    curses.endwin()
 
if __name__ == "__main__":
    curses.wrapper(main)