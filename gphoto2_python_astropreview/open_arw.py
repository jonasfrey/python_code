import rawpy 
import cv2
import numpy
import pyautogui
import keyboard
# from pynput.mouse import Listener


# # This function will be called when any key of mouse is pressed
# def on_click(*args):
#     # see what argument is passed.
#     print(args)
#     if args[-1]:
#         # Do something when the mouse key is pressed.
#         print('The "{}" mouse key has held down'.format(args[-2].name))

#     elif not args[-1]:
#         # Do something when the mouse key is released.
#         # Do something when the mouse key is released.
#         print('The "{}" mouse key is released'.format(args[-2].name))

# with Listener(on_click=on_click) as listener:
#     # Listen to the mouse key presses
#     listener.join()



a_screen_size = pyautogui.size()
n_screen_width = a_screen_size[0]
n_screen_height = a_screen_size[1]

s_path_file_name = "./tmp.arw"
o_img_raw = rawpy.imread(s_path_file_name)
n_bit_depth = o_img_raw.raw_image.dtype
dt = numpy.dtype(o_img_raw.raw_image.dtype)
n_bytes = dt.itemsize
n_bits = n_bytes * 8
n_value_max = pow(2, n_bits)-1
print(n_value_max)
n_resize_factor = 0.2
o_img_raw_resized = cv2.resize(
    o_img_raw.raw_image,
    (
        int(o_img_raw.raw_image.shape[1]*n_resize_factor),
        int(o_img_raw.raw_image.shape[0]*n_resize_factor)
        ), 
    interpolation= cv2.INTER_LINEAR
    )
# o_img_cv2 = cv2.imread(o_img_raw_resized)
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
cv2.imshow(s_path_file_name, o_img_raw_resized*1)
keyCode = cv2.waitKey(1)

# exit()
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)
# o_img_raw_resized = cv2.merge([o_img_raw_resized,o_img_raw_resized,o_img_raw_resized])

a_s_menu_option = [
    "0|brightness", 
    "0|gamma"
]
n_index_a_s_menu_option = 0

def f_cv2_put_text(
    a_s_line,
    a_img, 
    b_double_outline = False
    ):

    n_font = cv2.FONT_HERSHEY_SIMPLEX
    # n_font = cv2.FONT_HERSHEY_PLAIN
    a_point = (50, 50)
    a_color = (0,0,int(0.3*n_value_max))
    a_color_outline = (0,0,int(0.1*n_value_max))
    a_color_bw = (12,12,12)
    a_color_outline_bw = (n_value_max*0.5,n_value_max*0.5,n_value_max*0.5)

    n_thickness = 1
    n_font_scale = 1
    n_margin = 10
    n_line_height = n_font_scale 
    a_text_size = cv2.getTextSize(
        text=str(a_s_line[0]),
        fontFace=n_font,
        fontScale=n_font_scale,
        thickness=n_thickness
    )
    for n_i, s_line in enumerate(a_s_line): 

        # a_point[1] += a_text_size[1] * n_i
        a_point = (a_point[0], a_point[1] + a_text_size[0][1] * n_i+n_margin)
        if(b_double_outline):
            cv2.putText(
                a_img,
                s_line,
                a_point,
                n_font,
                n_font_scale,
                a_color_outline_bw,
                thickness = n_thickness+3
            )
        cv2.putText(
                a_img,
                s_line,
                a_point,
                n_font,
                n_font_scale,
                a_color_outline_bw,
                thickness = n_thickness+2
            )
        cv2.putText(
                a_img,
                s_line,
                a_point,
                n_font,
                n_font_scale,
                a_color_bw,
                thickness = n_thickness
            )

# print(o_img_raw_resized.ndim)
n_factor = 2
s_window_name = "o_img_raw_resized"

b_space_down = False 
b_space_down_last = False
while True: 


    if keyboard.is_pressed("space"):  # if key 'q' is pressed 
        b_space_down = True

    o_img_raw_copy = o_img_raw_resized.copy()

    if(b_space_down and b_space_down_last == False):
        n_index_a_s_menu_option = (n_index_a_s_menu_option+1)%len(a_s_menu_option)

    a_pos_mouse = pyautogui.position()

    n_mouse_x_normalized = a_pos_mouse[0] / n_screen_width
    n_mouse_y_normalized = a_pos_mouse[1] / n_screen_height

    a_s_line = []
    a_s_line.append('\033[1mYOUR_STRING\033[0m')
    a_s_line.append('not bold')
    a_s_line.append('x:'+str(n_mouse_x_normalized))
    a_s_line.append('y:'+str(n_mouse_y_normalized))

    o_img_raw_copy = o_img_raw_copy + int(n_value_max*n_mouse_y_normalized)

    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    f_cv2_put_text(a_s_line, o_img_raw_copy)
    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    cv2.imshow(s_window_name, o_img_raw_copy)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
            break

    b_space_down_last = b_space_down
cv2.destroyAllWindows()