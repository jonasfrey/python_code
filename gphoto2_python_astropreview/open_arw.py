from dataclasses import dataclass


import rawpy 
import cv2
import numpy
import pyautogui
import keyboard
# from pynput.mouse import Listener
import subprocess
import time
import os
import rawpy
import cv2



def f_a_n_video_devices_numbers():

    s_test = f_run_bash_command(["ls","/dev/video*"], True)
    print(s_test)

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


@dataclass
class O_menu_option:
    s_identification_string: str
    s_name: str
    a_n_index_value: list
    a_s_name_value: list
    s_value: str
    n_mouse_x_normalized: float
    n_mouse_y_normalized: float

a_o_menu_option = [
    O_menu_option(
        "gamma", 
        "0|gamma", 
        [],
        [],
        "not initialized",
        0.0,
        0.0 
    ),
    O_menu_option(
        "brightness",
        "0|brightness", 
        [],
        [],
        "not initialized",
        0.0,
        0.0 
    ), 
    O_menu_option(
        "shutter_speed", 
        "0|shutter speed", 
        [0,1,2],
        [
            "1/10s", 
            "2s", 
            "10s"
        ],
        "not initialized",
        0.0,
        0.0 
    ), 
    O_menu_option(
        "iso",
        "0|iso", 
        [0,1,2],
        [
            "50", 
            "6400", 
            "25600"
        ],
        "not initialized",
        0.0,
        0.0 
    ), 
    O_menu_option(
        "loop_capture",
        "0|loop capture", 
        [0,1],
        [
            "off", 
            "on"
        ],
        "not initialized",
        0.0,
        0.0 
    )
]
o_menu_option = O_menu_option(
        "camera",
        "0|camera", 
        [],
        [],
        "not initialized",
        0.0,
        0.0 
    )

a_n_video_devices_numbers = f_a_n_video_devices_numbers()
print(a_n_video_devices_numbers)
exit()
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

o_menu_option = a_o_menu_option[0]

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

    n_mouse_x_normalized = float(a_pos_mouse[0] / n_screen_width)
    n_mouse_y_normalized = float(a_pos_mouse[1] / n_screen_height)

    if(
        a_pos_mouse[0] != a_pos_mouse_last[0]
        or
        a_pos_mouse[1] != a_pos_mouse_last[1]
    ):
        # o_menu_option.n_mouse_x_normalized = n_mouse_x_normalized
        # o_menu_option.n_mouse_y_normalized = n_mouse_y_normalized
        o_menu_option.n_mouse_x_normalized = float(format(n_mouse_x_normalized, ".3f"))
        o_menu_option.n_mouse_y_normalized = float(format(n_mouse_y_normalized, ".3f"))

    print(o_menu_option.n_mouse_y_normalized)

    a_s_line = ["["+o.s_name+"]"+":"+o.s_value if(o == o_menu_option) else o.s_name + ":" + o.s_value for o in a_o_menu_option]

    # a_s_line.append(' '.join(a_s_line_menu_options))
    a_s_line.append('x|y'+str(format(n_mouse_x_normalized, ".3f"))+"|"+str(format(n_mouse_y_normalized, ".3f")))

    if(o_menu_option.s_identification_string == "brightness" ):
        o_menu_option.s_value = str(int(n_value_max*o_menu_option.n_mouse_y_normalized))
        o_img_raw_copy = o_img_raw_copy + int(n_value_max*o_menu_option.n_mouse_y_normalized)

    if(o_menu_option.s_identification_string == "contrast" ):
        o_menu_option.s_value = str(2 * o_menu_option.n_mouse_y_normalized)
        # o_img_raw_copy = o_img_raw_copy * 2*n_mouse_y_normalized
        o_img_raw_copy = (o_img_raw_copy * 2 * o_menu_option.n_mouse_y_normalized).astype(numpy.uint8)

        # print(type(o_img_raw_copy))
    if(o_menu_option.s_identification_string == "gamma" ):
        o_menu_option.s_value = str(5 * o_menu_option.n_mouse_y_normalized)
        # o_img_raw_copy = o_img_raw_copy * 2*n_mouse_y_normalized
        n_prevent_zero_devision = 0.00001
        o_img_raw_copy = adjust_gamma(o_img_raw_copy, (5 * o_menu_option.n_mouse_y_normalized) + n_prevent_zero_devision)


    if( o_menu_option.s_identification_string in ["shutter_speed", "iso", "loop_capture"]):
        n_index = int(o_menu_option.n_mouse_y_normalized * (len(o_menu_option.a_n_index_value))) 
        n_index_value = o_menu_option.a_n_index_value[n_index]
        s_name_value = o_menu_option.a_s_name_value[n_index]
        o_menu_option.s_value = s_name_value

    # if( o_menu_option.s_identification_string in ["loop_capture"]):
    #     n_index = int(o_menu_option.n_mouse_y_normalized > 0.5)
    #     n_index_value = o_menu_option.a_n_index_value[n_index]
    #     s_name_value = o_menu_option.a_s_name_value[n_index]
    #     o_menu_option.s_value = s_name_value

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