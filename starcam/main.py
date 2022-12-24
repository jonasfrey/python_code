


import subprocess
import pyautogui
import cv2

## requirements 
# sudo apt install python3-opencv
# pip3 install pyautogui

# s_command = "chromium-browser https://www.crackedthecode.co/how-to-use-your-dslr-as-a-webcam-in-linux/";
# list_dir = subprocess.Popen(s_command.split(" "));
# list_dir.wait()

# s_command = "sudo modprobe v4l2loopback exclusive_caps=1 max_buffers=2 && gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video0";
# list_dir = subprocess.Popen(s_command.split(" "));
# list_dir.wait()

cv2.namedWindow("preview")
o_cam = cv2.VideoCapture(0)

if o_cam.isOpened(): # try to get the first frame
    o_error, a_frame = o_cam.read()
else:
    o_error = False

n_screen_width, n_screen_height = pyautogui.size()
n_factor = 2

while o_error:
    n_mouse = pyautogui.position()
    n_mouse_x = n_mouse[0]
    n_mouse_y = n_mouse[1]
    n_mouse_x_normalized =  (n_mouse_x+1) /n_screen_width
    n_mouse_y_normalized = (n_mouse_y+1) / n_screen_height

    print("n_mouse_x_normalized")
    print(n_mouse_x_normalized)
    
    a_frame = a_frame * (n_mouse_x_normalized) * n_factor#prevent division by 0

    cv2.imshow("press escape (esc) to exit!!!", a_frame)
    o_error, a_frame = o_cam.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")