from re import I
import rawpy 
import cv2
import numpy
import pyautogui
import keyboard
from matplotlib import pyplot as plt
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
o_img_8bit = (o_img_raw.raw_image/256).astype(numpy.uint8)
dt = numpy.dtype(o_img_8bit.dtype)
n_bytes = dt.itemsize
n_bits = n_bytes * 8
n_value_max = pow(2, n_bits)-1
print(n_value_max)
n_resize_factor = 0.2
o_img_raw_resized = cv2.resize(
    o_img_8bit,
    (
        int(o_img_8bit.shape[1]*n_resize_factor),
        int(o_img_8bit.shape[0]*n_resize_factor)
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

s_menu_option_brightness = "0|brightness"
s_menu_option_gamma = "0|gamma"
s_menu_option_contrast = "0|contrast"

a_s_menu_option = [
    s_menu_option_brightness,
    s_menu_option_gamma,
    s_menu_option_contrast,
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
s_menu_option = a_s_menu_option[n_index_a_s_menu_option]

# plt.hist(o_img_raw_resized.ravel(),n_value_max,[0,n_value_max]); plt.show()


cv2.imwrite( "o_img_raw_resized.jpg", o_img_raw_resized)


def f_a_img_histogram(
    a_img
):
    n_value_max = 255
    histogram = cv2.calcHist([a_img], [0], None, [n_value_max], [0, n_value_max])
    n_histogram_max = numpy.max(histogram)
    n_height_img_histogram = 100
    n_width_img_histogram = n_value_max
    a_img_histogram = numpy.zeros([n_height_img_histogram, n_width_img_histogram],dtype=numpy.uint8)
    # print(n_histogram_max)
    # print(histogram)
    for n_index, n_value in enumerate(histogram):
        a_img_histogram[
            n_height_img_histogram-int((n_value/n_histogram_max)*n_height_img_histogram): n_height_img_histogram, 
            n_index:n_index+1
            ] = n_value_max

    return a_img_histogram



# cv2.imwrite( "histogram.jpg", f_a_img_histogram(o_img_raw_resized))
# keyCode = cv2.waitKey(1)




# exit()
while True: 


    if keyboard.is_pressed("space"):  # if key 'q' is pressed 
        b_space_down = True
    else:
        b_space_down = False

    o_img_raw_copy = o_img_raw_resized.copy()

    if(b_space_down and b_space_down_last == False):
        n_index_a_s_menu_option = (n_index_a_s_menu_option+1)%len(a_s_menu_option)
        s_menu_option = a_s_menu_option[n_index_a_s_menu_option]

    a_pos_mouse = pyautogui.position()

    n_mouse_x_normalized = a_pos_mouse[0] / n_screen_width
    n_mouse_y_normalized = a_pos_mouse[1] / n_screen_height

    a_s_line = []
    a_s_line_menu_options = a_s_menu_option.copy()
    a_s_line_menu_options[n_index_a_s_menu_option] = "["+a_s_line_menu_options[n_index_a_s_menu_option]+"]"

    a_s_line.append(' '.join(a_s_line_menu_options))
    a_s_line.append('x:'+str(n_mouse_x_normalized))
    a_s_line.append('y:'+str(n_mouse_y_normalized))

    if(s_menu_option == s_menu_option_brightness):
        o_img_raw_copy = o_img_raw_copy + int(n_value_max*n_mouse_y_normalized)
    if(s_menu_option == s_menu_option_contrast):
        # o_img_raw_copy = o_img_raw_copy * 2*n_mouse_y_normalized
        o_img_raw_copy = (o_img_raw_copy * 2 * n_mouse_y_normalized).astype(numpy.uint8)
        print(type(o_img_raw_copy))
        # o_img_raw_copy = numpy.multiply(o_img_raw_copy, [1.01])
    # if(s_menu_option == s_menu_option_gamma):
    #     o_img_raw_copy = o_img_raw_copy + int(n_value_max*n_mouse_y_normalized)

    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)
    a_histogram = f_a_img_histogram(o_img_raw_copy)
    cv2.imshow( "histogram", a_histogram)

    f_cv2_put_text(a_s_line, o_img_raw_copy)
    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    print(o_img_raw_copy.shape)
    print(a_histogram.shape)

    # o_img_raw_copy = cv2.addWeighted(o_img_raw_copy,0.4,a_histogram,0.1,0)
    o_img_raw_copy[
        o_img_raw_copy.shape[0]-a_histogram.shape[0]:o_img_raw_copy.shape[0],
        o_img_raw_copy.shape[1]-a_histogram.shape[1]:o_img_raw_copy.shape[1]
        ] = a_histogram

    cv2.imshow(s_window_name, o_img_raw_copy)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
            break

    b_space_down_last = b_space_down
cv2.destroyAllWindows()