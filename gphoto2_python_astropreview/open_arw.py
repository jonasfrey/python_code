import rawpy 
import cv2
import numpy
import pyautogui
import keyboard
from matplotlib import pyplot as plt
# from pynput.mouse import Listener

import subprocess
import time
import os
import rawpy
import cv2


def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = numpy.array([((i / 255.0) ** invGamma) * 255
		for i in numpy.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

def f_run_bash_command(a_binary_and_arguments, b_output_is_text = False):
    print("running bash command:")
    print(" ".join(a_binary_and_arguments))
    process = subprocess.Popen(
        a_binary_and_arguments,
        stdout=subprocess.PIPE, 
        text=b_output_is_text
        )
    # run bash command

    s_command_output, error = process.communicate()

    # print(error)
    # print(str(s_command_output))

    return s_command_output


def f_detect_cameras():
    s_command_output = f_run_bash_command(['gphoto2', '--auto-detect'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)
    # print(len(a_lines))
    if(len(a_lines) < 4):
        print('no cameras detected ! ')
    
def f_list_config():
    s_command_output = f_run_bash_command(['gphoto2', '--list-config'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_read_config(s_name):
    s_command_output = f_run_bash_command(['gphoto2', '--get-config', s_name], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_write_config_index(s_name, s_value):
    s_command_output = f_run_bash_command(['gphoto2', '--set-config', s_name+'='+str(s_value)], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)

def f_write_config_value(s_name, s_value):
    s_command_output = f_run_bash_command(['gphoto2', '--set-config-value', s_name+'="'+str(s_value)+'"'], True)
    a_lines = s_command_output.split("\n")
    print(s_command_output)


def f_capture_and_download(
    s_path_file_name
):
    try:
        os.remove(s_path_file_name)
    except:
        pass
    ts = str(int(time.time()))
    s_command_output = f_run_bash_command(['gphoto2','--capture-image-and-download', '--filename', str(s_path_file_name)], True)

    a_lines = s_command_output.split("\n")
    print(s_command_output)

def f_n_ts_ms():
    return round(time.time() * 1000)


a_screen_size = pyautogui.size()
n_screen_width = a_screen_size[0]
n_screen_height = a_screen_size[1]

# s_path_file_name = "./tmp.arw"
# o_img_raw = rawpy.imread(s_path_file_name)
# o_img_8bit = (o_img_raw.raw_image/256).astype(numpy.uint8)
# dt = numpy.dtype(o_img_8bit.dtype)
# n_bytes = dt.itemsize
# n_bits = n_bytes * 8
# n_value_max = pow(2, n_bits)-1
# print(n_value_max)
# n_resize_factor = 0.2
# o_img_raw_resized = cv2.resize(
#     o_img_8bit,
#     (
#         int(o_img_8bit.shape[1]*n_resize_factor),
#         int(o_img_8bit.shape[0]*n_resize_factor)
#         ), 
#     interpolation= cv2.INTER_LINEAR
#     )
# o_img_cv2 = cv2.imread(o_img_raw_resized)
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
# cv2.imshow(s_path_file_name, o_img_raw_resized*1)
# keyCode = cv2.waitKey(1)

def f_o_img_resized(s_path_file_name):

    if(os.path.isfile(s_path_file_name) == False):
        o_img_raw_resized = numpy.zeros([500,500],dtype=numpy.uint8)
    else: 
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


    return o_img_raw_resized
# exit()
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)
# o_img_raw_resized = cv2.merge([o_img_raw_resized,o_img_raw_resized,o_img_raw_resized])



class O_menu_option:
    s_name: str
    a_value_n_index: list
    a_value_s_name: list
    n_value: int # will be used as index for a_value

a_o_menu_option = [
    O_menu_option(
        "0|gamma", 
        [],
        [],
        0, 
    ),
    O_menu_option(
        "0|brightness", 
        [],
        [],
        0, 
    ),
    O_menu_option(
        "0|brightness", 
        [],
        [],
        0, 
    ), 
    O_menu_option(
        "0|shutter speed", 
        [0,1,2],
        [
            "1/10s", 
            "2s", 
            "10s"
        ],
        0, 
    ), 
    O_menu_option(
        "0|iso", 
        [0,1,2],
        [
            "1/10s", 
            "2s", 
            "10s"
        ],
        0, 
    ), 
    O_menu_option(
        "0|loop_capture", 
        [0,1],
        [
            "off", 
            "on"
        ],
        0, 
    )
]

    

o_array_string_options = {
    "o_shutter_speed": {
        "s_menu_option_name": "0|shutter speed", 
        "n_index": 0, 
        "a_n_index": [0,1,2], 
        "a_s_name": [
                "1/10s", 
                "2s", 
                "10s"
            ]
    },
    "o_iso": {
       "s_menu_option_name": "0|iso", 
       "n_index": 0, 
       "a_n_index": [0,1,2], 
       "a_s_name": [
            "50", 
             "6400", 
            "25600"
        ]
   },
    "o_loop_capture": {
       "s_menu_option_name": "0|loop capture", 
       "n_index": 0, 
       "a_n_index": [0,1], 
       "a_s_name": [
            "off", 
            "on", 
        ]
   } 
}



a_s_menu_option_values = []
for n in a_s_menu_option:
    a_s_menu_option_values.append("null")

def f_cv2_put_text(
    a_s_line,
    a_img, 
    b_double_outline = False
    ):

    n_font = cv2.FONT_HERSHEY_SIMPLEX
    # n_font = cv2.FONT_HERSHEY_PLAIN
    n_margin_x = 50
    n_margin_y = 100
    a_color = (0,0,int(0.3*n_value_max))
    a_color_outline = (0,0,int(0.1*n_value_max))
    a_color_bw = (12,12,12)
    a_color_outline_bw = (n_value_max*0.5,n_value_max*0.5,n_value_max*0.5)

    n_thickness = 1
    n_font_scale = 1
    n_margin = 20
    n_line_height = n_font_scale 
    a_text_size = cv2.getTextSize(
        text=str(a_s_line[0]),
        fontFace=n_font,
        fontScale=n_font_scale,
        thickness=n_thickness
    )
    for n_i, s_line in enumerate(a_s_line): 

        # a_point[1] += a_text_size[1] * n_i
        # a_point = (a_point[0], a_point[1] + a_text_size[0][1] * n_i+n_margin)
        a_point_new = (n_margin_x, n_margin_y + n_i*(a_text_size[0][1]+n_margin))
        if(b_double_outline):
            cv2.putText(
                a_img,
                s_line,
                a_point_new,
                n_font,
                n_font_scale,
                a_color_outline_bw,
                thickness = n_thickness+3
            )
        cv2.putText(
                a_img,
                s_line,
                a_point_new,
                n_font,
                n_font_scale,
                a_color_outline_bw,
                thickness = n_thickness+2
            )
        cv2.putText(
                a_img,
                s_line,
                a_point_new,
                n_font,
                n_font_scale,
                a_color_bw,
                thickness = n_thickness
            )

# print(o_img_raw_resized.ndim)
n_factor = 2
s_window_name = "o_img_raw_resized"

n_index_a_o_menu_option = 0

s_menu_option = a_o_menu_option[n_index_a_o_menu_option]

# plt.hist(o_img_raw_resized.ravel(),n_value_max,[0,n_value_max]); plt.show()


# cv2.imwrite( "o_img_raw_resized.jpg", o_img_raw_resized)

n_value_max = 255


def f_a_img_histogram(
    a_img
):
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


a_pos_mouse = pyautogui.position()
a_pos_mouse_last = pyautogui.position()


s_path_file_name = "./tmpcap.arw"

b_enter_down = False
o_keyboard_keys = {
    "enter": {
        "b_down": False, 
        "b_down_last": False, 
        "b_down_oneshot": False, 
        "s_is_pressed_name": "enter"
    },
    "space": {
        "b_down": False, 
        "b_down_last": False, 
        "b_down_oneshot": False, 
        "s_is_pressed_name": "space"
    },
}   
# exit()
o_img_raw_resized = f_o_img_resized(s_path_file_name)
n_frame_id = 0
while True: 
    print("n_frame_id")
    print(n_frame_id)
    n_frame_id+= 1

    for s_prop in o_keyboard_keys: 
        o_keyboard_key = o_keyboard_keys[s_prop]
        if keyboard.is_pressed(o_keyboard_key["s_is_pressed_name"]):  # if key 'q' is pressed 
            o_keyboard_key["b_down"] = True
        else:
            o_keyboard_key["b_down"] = False

    for s_prop in o_keyboard_keys: 
        o_keyboard_key = o_keyboard_keys[s_prop]
        if(o_keyboard_key["b_down"] == True and o_keyboard_key["b_down_last"] == False):
            o_keyboard_key["b_down_oneshot"] = True
        else: 
            o_keyboard_key["b_down_oneshot"] = False

    o_img_raw_copy = o_img_raw_resized.copy()

    if(o_keyboard_keys["space"]["b_down_oneshot"]):
        n_index_a_o_menu_option = (n_index_a_o_menu_option+1)%len(a_o_menu_option)
        o_menu_option = a_o_menu_option[n_index_a_o_menu_option]

    if(o_keyboard_keys["enter"]["b_down_oneshot"]):
        f_capture_and_download(s_path_file_name)
        o_img_raw_resized = f_o_img_resized(s_path_file_name)
    # if(n_frame_id == 100):
    #     f_capture_and_download(s_path_file_name)
    #     o_img_raw_resized = f_o_img_resized(s_path_file_name)
    
    a_pos_mouse = pyautogui.position()

    n_mouse_x_normalized = a_pos_mouse[0] / n_screen_width
    n_mouse_y_normalized = a_pos_mouse[1] / n_screen_height

    a_s_line = [if() o.s_name for o in a_o_menu_option]

    a_s_line_menu_options = a_s_menu_option.copy()
    a_s_line_menu_options[n_index_a_s_menu_option] = "["+a_s_line_menu_options[n_index_a_s_menu_option]+"]"
    # a_s_line.append(' '.join(a_s_line_menu_options))
    a_s_line.append('x|y'+str(format(n_mouse_x_normalized, ".3f"))+"|"+str(format(n_mouse_y_normalized, ".3f")))

    for n_index, value in enumerate(a_s_menu_option):
        s_value = value + a_s_menu_option_values[n_index]
        if(n_index == n_index_a_s_menu_option): 
            s_value = "["+s_value+"]"
        
        a_s_line.append(s_value)

    if(s_menu_option == s_menu_option_brightness):
        o_img_raw_copy = o_img_raw_copy + int(n_value_max*n_mouse_y_normalized)
        a_s_menu_option_values[n_index_a_s_menu_option] = str(int(n_value_max*n_mouse_y_normalized))

    if(s_menu_option == s_menu_option_contrast):
        # o_img_raw_copy = o_img_raw_copy * 2*n_mouse_y_normalized
        o_img_raw_copy = (o_img_raw_copy * 2 * n_mouse_y_normalized).astype(numpy.uint8)
        # print(type(o_img_raw_copy))
        a_s_menu_option_values[n_index_a_s_menu_option] = str(int(2 * n_mouse_y_normalized))
    if(s_menu_option == s_menu_option_gamma):

        # o_img_raw_copy = o_img_raw_copy * 2*n_mouse_y_normalized
        o_img_raw_copy = adjust_gamma(o_img_raw_copy, 5 * n_mouse_y_normalized)

    if(
        a_pos_mouse[0] != a_pos_mouse_last[0]
        or
        a_pos_mouse[1] != a_pos_mouse_last[1]
    ):
        # allow toggling the values without changing them when mouse has no new position 

        for s_prop in o_array_string_options:
            o_array_string_option = o_array_string_options[s_prop]
            # print(o_array_string_option)
            if(s_menu_option == o_array_string_option["s_menu_option_name"]):
                o_array_string_option["n_index"] = int(n_mouse_y_normalized * len(o_array_string_option["a_n_index"]))
                # a_s_line.append(o_array_string_option["s_menu_option_name"]+':'+str(o_array_string_option["a_s_name"][o_array_string_option["n_index"]]))
                a_s_menu_option_values[n_index_a_s_menu_option] = str(o_array_string_option["a_s_name"][o_array_string_option["n_index"]])


            # o_img_raw_copy = numpy.multiply(o_img_raw_copy, [1.01])
        # if(s_menu_option == s_menu_option_gamma):
        #     o_img_raw_copy = o_img_raw_copy + int(n_value_max*n_mouse_y_normalized)

    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)
    a_histogram = f_a_img_histogram(o_img_raw_copy)
    cv2.imshow( "histogram", a_histogram)

    f_cv2_put_text(a_s_line, o_img_raw_copy)
    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    for s_prop in o_keyboard_keys: 
        o_keyboard_key = o_keyboard_keys[s_prop]
        o_keyboard_key["b_down_last"] = o_keyboard_key["b_down"]


    # print(o_img_raw_copy.shape)
    # print(a_histogram.shape)

    # o_img_raw_copy = cv2.addWeighted(o_img_raw_copy,0.4,a_histogram,0.1,0)
    o_img_raw_copy[
        o_img_raw_copy.shape[0]-a_histogram.shape[0]:o_img_raw_copy.shape[0],
        o_img_raw_copy.shape[1]-a_histogram.shape[1]:o_img_raw_copy.shape[1]
        ] = a_histogram

    cv2.imshow(s_window_name, o_img_raw_copy)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
            break


    a_pos_mouse_last = a_pos_mouse

cv2.destroyAllWindows()