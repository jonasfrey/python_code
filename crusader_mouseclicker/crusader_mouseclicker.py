# # from pymouse import PyMouse



# # o_mouse = PyMouse()
# # o_mouse.position() #gets mouse current position coordinates
# # o_mouse.move(500,500)
# # o_mouse.click(500,500, 1) #the third argument "1" represents the mouse button
# # # o_mouse.press(x,y) #mouse button press
# # o_mouse.release(500,500) #mouse button release

# import pyautogui

# pyautogui.click(500, 500)
# # pyautogui.moveTo(100, 150)
# # pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
# # pyautogui.dragTo(100, 150)
# # pyautogui.dragRel(0, 10)  # drag mouse 10 pixels down

import mouse
# left click
import time
import pyautogui

from pynput.mouse import Button, Controller

# def click_pynput(x, y, button):
#     mouse = Controller()
#     mouse.position = (x, y)
#     button = Button.left if button=='left' else Button.right
#     mouse.click(Button.left)

# pyautogui.moveTo(x,y)

# time.sleep(0.5) #or whatever you need, if even needed

import keyboard  # using module keyboard
while 1:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('esc'):  # if key 'q' is pressed 
            print('exiiting program')
            break  # finishing the loop
        if keyboard.is_pressed('e'):  # if key 'q' is pressed
            # pyautogui.mouseDown()
            # pyautogui.mouseUp()
            o_mouse = Controller()
            o_mouse.click(Button.left)
            time.sleep(0.1)

            # pyautogui.click(button="left")

            print('click event exeecuted')
    except:
        break  # if user pressed a key other than the given key the loop will break

# mouse.drag(0, 0, 100, 100, absolute=False, duration=0.1)

