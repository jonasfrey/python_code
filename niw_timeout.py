import sys
import sys, tty, termios
from select import select

timeout = 0.5
print ("Enter something:")
rlist, _, _ = select([sys.stdin], [], [], timeout)
if rlist:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setraw(sys.stdin.fileno())

    ch = sys.stdin.read(1)
else:
    print ("No input. Moving on...")