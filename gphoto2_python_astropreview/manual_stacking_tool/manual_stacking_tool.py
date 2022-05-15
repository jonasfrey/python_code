import cv2
from scipy import signal
from scipy import misc
import numpy
import pyautogui
import os 
from dataclasses import dataclass
import keyboard
import PySimpleGUI as sg



# print(o_menu_option_camera)
def f_cv2_put_text(
    a_s_line,
    a_img, 
    b_double_outline = False
    ):

    n_font = cv2.FONT_HERSHEY_SIMPLEX
    # n_font = cv2.FONT_HERSHEY_PLAIN
    n_margin_x = 50
    n_margin_y = 100
    n_margin_x = cv2.getWindowImageRect(s_window_name)[0]
    n_margin_y = cv2.getWindowImageRect(s_window_name)[1]
    print(n_margin_x)
    print(n_margin_y)

    dt = a_img.dtype
    n_bytes = dt.itemsize
    n_bits = n_bytes * 8
    n_value_max = pow(2, n_bits)-1
    
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


a_screen_size = pyautogui.size()
n_screen_width = a_screen_size[0]
n_screen_height = a_screen_size[1]



class O_menu_option:
    def __init__(
        self,
        s_identification_string: str,
        s_name: str,
        a_s_name_value: list,
        n_value: str,
        s_value: str,
        n_mouse_x_normalized: float,
        n_mouse_y_normalized: float,
        # n_mouse_x_normalized_last: float,
        # n_mouse_y_normalized_last: float,
        # n_mouse_x_normalized_delta: float,
        # n_mouse_y_normalized_delta: float

) -> None:
        self.s_identification_string = s_identification_string
        self.s_name = s_name
        self.a_s_name_value = a_s_name_value
        self.n_value = n_value
        self.s_value = s_value
        self.n_mouse_x_normalized = n_mouse_x_normalized
        self.n_mouse_y_normalized = n_mouse_y_normalized
        self.n_mouse_x_normalized_last = 0
        self.n_mouse_y_normalized_last = 0
        self.n_mouse_x_normalized_delta = 0
        self.n_mouse_y_normalized_delta = 0
        self.n_mouse_x_normalized_frozen = 0
        self.n_mouse_y_normalized_frozen = 0

        pass


class O_image:
    def __init__(
        self,
        s_path_file: str, 
        # a_img: numpy.ndarray
        ) -> None:
        self.s_path_file = s_path_file
        self.a_image = cv2.imread(self.s_path_file)
        self.n_transformation_translation_x = 0
        self.n_transformation_translation_y = 0
        self.n_transformation_rotation = 0
        self.n_transformation_scale_x = 0
        self.n_transformation_scale_y = 0
        pass

a_o_image = []
s_path_images = './images/'
for s_file in os.listdir(s_path_images):
    s_file_path = os.path.join(s_path_images, s_file)
    print(s_file_path)
    if os.path.isfile(s_file_path):
        a_o_image.append(
            O_image(
                s_file_path
            )
        )


a_o_menu_option = []

o_menu_option_image = O_menu_option(
    "image",
    "0|image", 
    [],
    0.0,
    "not initialized",
    0.0,
    0.0
)
o_menu_option_image.a_s_name_value = [o.s_path_file for o in a_o_image]
a_o_menu_option.append(o_menu_option_image)

o_menu_option_image_reference = O_menu_option(
    "image_reference",
    "0|image_reference", 
    [],
    0.0,
    "not initialized",
    0.0,
    0.0 
)
o_menu_option_image_reference.a_s_name_value = [o.s_path_file for o in a_o_image]
a_o_menu_option.append(o_menu_option_image_reference)



o_menu_option_transform_translate = O_menu_option(
    "transform_translate",
    "transfrm_trnslt_x|trnsfrm_trsnlt_y", 
    [],
    0.0,
    "not initialized",
    0.0,
    0.0 
)
a_o_menu_option.append(o_menu_option_transform_translate)

o_menu_option_transform_rotate = O_menu_option(
    "transform_rotate",
    "transform_rotate|", 
    [],
    0.0,
    "not initialized",
    0.0,
    0.0 
)
a_o_menu_option.append(o_menu_option_transform_rotate)

o_menu_option_transform_scale = O_menu_option(
    "transform_scale",
    "trnsfrm_scl_x|trnsfrm_scl_y", 
    [],
    0.0,
    "not initialized",
    0.0,
    0.0 
)
a_o_menu_option.append(o_menu_option_transform_scale)


a_pos_mouse = pyautogui.position()
a_pos_mouse_last = pyautogui.position()
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
    "p": {
        "b_down": False, 
        "b_down_last": False, 
        "b_down_oneshot": False, 
        "s_is_pressed_name": "p"
    },
}


n_index_a_o_menu_option = 0
o_menu_option = a_o_menu_option[n_index_a_o_menu_option]
n_frame_id = 0
s_window_name = __file__
cv2.namedWindow(s_window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(s_window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

a_layout = []
for o in a_o_menu_option:
    a_layout.append(
        [sg.Text(o.s_name, key=o.s_identification_string)]
    )
o_window = sg.Window(
    keep_on_top=True, 
    title=s_window_name,
    layout=a_layout,
    margins=(100, 50),
    finalize=True
    )
o_window.read(timeout=1)


def f_pass():
    pass

for o in a_o_menu_option: 

    # cv2.createButton("Back",f_pass,None,cv2.QT_PUSH_BUTTON,1)
    cv2.createTrackbar(o.s_name.ljust(200, " "), s_window_name, 0, 1, f_pass)

o_test = cv2.createTrackbar("o_test".ljust(100, " "), s_window_name, 0, 1, f_pass)
# cv2.setTrackbarPos("o_test", 50)
# print(o_test)
# exit()
while True: 
    # print("n_frame_id")
    # print(n_frame_id)
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

    if(o_keyboard_keys["space"]["b_down_oneshot"]):
        n_index_a_o_menu_option = (n_index_a_o_menu_option+1)%len(a_o_menu_option)
        
        o_menu_option = a_o_menu_option[n_index_a_o_menu_option]

    a_o_image_filtered =  [o for o in a_o_image if o.s_path_file == o_menu_option_image.s_value]
    if(len(a_o_image_filtered) == 0):
        a_o_image_filtered = a_o_image
    o_image = a_o_image_filtered[0]
    # a_o_image[int(o_menu_option_image.n_value)]
    o_image_a_image_copy = o_image.a_image.copy()

    a_o_image_reference_filtered =  [o for o in a_o_image if o.s_path_file == o_menu_option_image_reference.s_value]
    if(len(a_o_image_reference_filtered) == 0):
        a_o_image_reference_filtered = a_o_image
    o_image_reference = a_o_image_reference_filtered[0]

    # if(n_frame_id == 100):
    #     f_capture_and_download(s_path_file_name)
    #     o_img_raw_resized = f_o_img_resized(s_path_file_name)
    a_pos_mouse = pyautogui.position()

    n_mouse_x_normalized = float(a_pos_mouse[0] / n_screen_width)
    n_mouse_y_normalized = float(a_pos_mouse[1] / n_screen_height)

    o_menu_option.n_mouse_x_normalized_last = o_menu_option.n_mouse_x_normalized
    o_menu_option.n_mouse_y_normalized_last = o_menu_option.n_mouse_y_normalized

    o_menu_option.n_mouse_x_normalized = n_mouse_x_normalized
    o_menu_option.n_mouse_y_normalized = n_mouse_y_normalized
    
    o_menu_option.n_mouse_x_normalized_delta = o_menu_option.n_mouse_x_normalized_last - o_menu_option.n_mouse_x_normalized
    o_menu_option.n_mouse_y_normalized_delta = o_menu_option.n_mouse_y_normalized_last - o_menu_option.n_mouse_y_normalized

    if(
        a_pos_mouse[0] != a_pos_mouse_last[0]
        or
        a_pos_mouse[1] != a_pos_mouse_last[1]
    ):
        # frozen mouse position does only change when the mouse delta has changed 
        # this allows for toggling through menu options and changing the values for each option independent
        o_menu_option.n_mouse_x_normalized_frozen = float(format(n_mouse_x_normalized, ".3f"))
        o_menu_option.n_mouse_y_normalized_frozen = float(format(n_mouse_y_normalized, ".3f"))

    # print(o_menu_option.n_mouse_y_normalized)

    if(o_menu_option.s_identification_string == "transform_translate" ):
        if(o_keyboard_keys["enter"]["b_down"]):
            o_image.n_transformation_translation_x = o_image.n_transformation_translation_x - (o_menu_option.n_mouse_x_normalized_delta*100)
            o_image.n_transformation_translation_y = o_image.n_transformation_translation_y - (o_menu_option.n_mouse_y_normalized_delta*100)

        

    if( o_menu_option.s_identification_string in ["image", "image_reference"]):
        n_index = int(o_menu_option.n_mouse_y_normalized_frozen * (len(o_menu_option.a_s_name_value)-0.00001)) 
        # n_index_value = o_menu_option.a_n_index_value[n_index]
        s_name_value = o_menu_option.a_s_name_value[n_index]
        o_menu_option.s_value = str(s_name_value)

    # a_s_line = ["["+o.s_name+"]"+":"+o.s_value if(o == o_menu_option) else o.s_name + ":" + o.s_value for o in a_o_menu_option]
    # a_s_line.append('x|y'+str(format(n_mouse_x_normalized, ".3f"))+"|"+str(format(n_mouse_y_normalized, ".3f")))
    # f_cv2_put_text(a_s_line, o_image_a_image_copy)
    for o in a_o_menu_option: 
        s = o.s_name + ":" + str(o.s_value)
        if(o == o_menu_option):
            s = "["+ s +"]"

        o_window[o.s_identification_string].update(s)
    
    event, values = o_window.read(timeout=1)


    for s_prop in o_keyboard_keys: 
        o_keyboard_key = o_keyboard_keys[s_prop]
        o_keyboard_key["b_down_last"] = o_keyboard_key["b_down"]

    
    if(o_keyboard_keys["p"]["b_down_oneshot"]):
        dt = a_o_image[0].a_image.dtype
        n_bytes = dt.itemsize
        n_bits = n_bytes * 8
        n_value_max = pow(2, n_bits)-1
        a_sum_image_normalized = (a_o_image[0].a_image / n_value_max).astype(numpy.float32)
        n_i = 1
        while(n_i < len(a_o_image)):

            a_sum_image_normalized_n_i = (a_o_image[n_i].a_image / n_value_max).astype(numpy.float32)
            n_width = a_sum_image_normalized_n_i.shape[1]
            n_height = a_sum_image_normalized_n_i.shape[0]
            a_transformation_matrix = numpy.float32([[1,0,a_o_image[n_i].n_transformation_translation_x],[0,1,a_o_image[n_i].n_transformation_translation_y]])
            a_sum_image_normalized_n_i_transformed = cv2.warpAffine(a_sum_image_normalized_n_i,a_transformation_matrix,(n_width,n_height))

            a_sum_image_normalized = a_sum_image_normalized + a_sum_image_normalized_n_i_transformed
            n_i = n_i + 1

        a_sum_image_normalized_arithmetic_medium = a_sum_image_normalized / len(a_o_image)

        a_sum_image_unnormalized_arithmetic_medium = a_sum_image_normalized_arithmetic_medium * n_value_max
        cv2.imwrite("a_sum_image_unnormalized_arithmetic_medium.png", a_sum_image_unnormalized_arithmetic_medium)
        print("image saved!")

    n_width = o_image_a_image_copy.shape[1]
    n_height = o_image_a_image_copy.shape[0]

    a_transformation_matrix = numpy.float32([[1,0,o_image.n_transformation_translation_x],[0,1,o_image.n_transformation_translation_y]])
    a_img_original_transformed = cv2.warpAffine(o_image_a_image_copy,a_transformation_matrix,(n_width,n_height))

    a_img_difference = o_image_reference.a_image - a_img_original_transformed


    cv2.imshow(s_window_name, a_img_difference)
    keyCode = cv2.waitKey(1)

    if event == sg.WIN_CLOSED:
        break
    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
        break


    a_pos_mouse_last = a_pos_mouse

cv2.destroyAllWindows()

