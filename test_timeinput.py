import thread
import threading

def raw_input_with_timeout(prompt, timeout=30.0):
    print(prompt)
    timer = threading.Timer(timeout, thread.interrupt_main)
    astring = None
    try:
        timer.start()
        astring = raw_input(prompt)
    except KeyboardInterrupt:
        pass
    timer.cancel()
    return astring
