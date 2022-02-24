import keyboard  # using module keyboard

# # print(keyboard._canonical_names.canonical_names)

# def only_works_in_focused_terminal_not_in_background():
#     while True:  # making a loop
#         try:  # used try so that if user pressed other than the given key error will not be shown
#             if keyboard.is_pressed('p'):  # if key 'q' is pressed 
#                 print('You Pressed capslock Key!')
#                 break  # finishing the loop
#         except:
#             break  # if user pressed a key other than the given key the loop will break



from pynput.keyboard import Key, Listener, Controller

controller = Controller()
keydown_lock = False 
keyup_lock = False

def on_press(key):
    global keydown_lock
    global keyup_lock

    if(keydown_lock == False):
        print('{0} pressed'.format(key))
        keydown_lock = True
        controller.press('a')
        keydown_lock = False


def on_release(key):
    print('{0} release'.format(key))
    # controller.release(key)
    # if key == Key.esc:
    #     return False


with Listener(
    # suppress=True,
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
