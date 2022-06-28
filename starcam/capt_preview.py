
import subprocess
import pyautogui
import cv2

# gphoto2 --list-all-config
# /main/imgsettings/imageformatsd
# Label: Image Format SD
# Readonly: 0
# Type: RADIO
# Current: RAW + Large Fine JPEG
# Choice: 0 Large Fine JPEG
# Choice: 1 Large Normal JPEG
# Choice: 2 Medium Fine JPEG
# Choice: 3 Medium Normal JPEG
# Choice: 4 Small Fine JPEG
# Choice: 5 Small Normal JPEG
# Choice: 6 Smaller JPEG
# Choice: 7 Tiny JPEG
# Choice: 8 RAW + Large Fine JPEG
# Choice: 9 RAW
# END
#gphoto2 --set-config /main/imgsettings/imageformatsd=0

n_screen_width, n_screen_height = pyautogui.size()
n_factor = 2


while True: 


    s_filename = "capture_preview.jpg"
    s_command = "rm "+s_filename
    subprocess.run(s_command.split(" "))

    s_command = "gphoto2 --capture-preview"
    subprocess.run(s_command.split(" "))
    a_frame = cv2.imread(s_filename)

    n_mouse = pyautogui.position()
    n_mouse_x = n_mouse[0]
    n_mouse_y = n_mouse[1]
    n_mouse_x_normalized =  (n_mouse_x+1) /n_screen_width
    n_mouse_y_normalized = (n_mouse_y+1) / n_screen_height

    print("n_mouse_x_normalized")
    print(n_mouse_x_normalized)
    
    a_frame = a_frame * (n_mouse_x_normalized) * n_factor#prevent division by 0


    cv2.imshow("asdf", a_frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
