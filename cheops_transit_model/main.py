from copyreg import constructor
from curses import A_COLOR
import cv2
import numpy
import keyboard
import matplotlib.pyplot
# using time module
import math
import time
import random
import cv2
import math
import time
from O_graph import O_graph
from O_cv2_text import O_cv2_text
from O_video_device import O_video_device
from O_graph_render_object import O_graph_render_object
from O_keyboard_key_state import O_keyboard_key_state

from f_a_o_video_device import f_a_o_video_device



def f_n_normalized_average_in_torus(
    n_circles_center_x, 
    n_circles_center_y,
    n_circle_radius_outer, 
    n_circle_radius_inner,
    a_frame
):
    a_masked_with_torus = f_a_masked_with_torus(
        n_circles_center_x, 
        n_circles_center_y,
        n_circle_radius_outer, 
        n_circle_radius_inner,
        a_frame
    )
    # cv2.imshow("a_masked_with_torus", a_masked_with_torus)
    n_pixels_in_circle_outer = int(pow(n_circle_radius_outer,2) * math.pi)
    n_pixels_in_circle_inner = int(pow(n_circle_radius_inner,2) * math.pi)
    n_number_of_pixels_in_torus = n_pixels_in_circle_outer - n_pixels_in_circle_inner
    n_sum_a_masked_with_torus = numpy.sum(a_masked_with_torus)
    n_average = n_sum_a_masked_with_torus / n_number_of_pixels_in_torus
    n_max_value = numpy.iinfo(a_frame.dtype).max
    n_normalized = n_average / n_max_value

    a_color = (0,255,0)

    cv2.circle(
        a_frame,
        (n_circles_center_x,n_circles_center_y),
        n_circle_radius_outer,
        a_color,
    )
    cv2.circle(
        a_frame,
        (n_circles_center_x,n_circles_center_y),
        n_circle_radius_inner,
        a_color,
    )
    cv2.putText(
            a_frame, 
            f"avg n: {n_normalized:.2f}",
            (n_circles_center_x-n_circle_radius_outer,n_circles_center_y-n_circle_radius_outer),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.8,
            a_color,
            1
    )
    return n_normalized


def f_a_masked_with_torus(
    n_circle_center_x, 
    n_circle_center_y,
    n_circle_radius_outer,
    n_circle_radius_inner,
    a_frame
):
    a_masked_with_circle = f_a_masked_with_circle(
        n_circle_center_x, 
        n_circle_center_y,
        n_circle_radius_outer,
        a_frame 
    )
    cv2.circle(
        a_masked_with_circle,
        (n_circle_center_x,n_circle_center_y),
        n_circle_radius_inner,
        0,
        -1
    )
    a_masked_with_torus = a_masked_with_circle
    return a_masked_with_torus

def f_a_masked_with_circle(
    n_circle_center_x, 
    n_circle_center_y,
    n_circle_radius,
    a_frame
):
    a_mask = numpy.zeros(a_frame.shape[:2], dtype="uint8")
    cv2.circle(
        a_mask,
        (n_circle_center_x,n_circle_center_y),
        n_circle_radius,
        255,
        -1
    )
    a_masked = cv2.bitwise_and(a_frame, a_frame, mask=a_mask)
    # cv2.imshow("f_n_normalized_average_in_circle a_masked", a_masked)
    return a_masked


def f_n_normalized_average_in_square(
    n_center_x,
    n_center_y,
    n_width,
    n_height,
    a_frame
):
    a_color = (0,255,0)
    n_x = n_center_x - int(n_width/2)
    n_y = n_center_y - int(n_height/2)

    a_subframe = a_frame[n_y:n_y+n_height,n_x:n_x+n_width]
    n_average_subframe = numpy.average(a_subframe)
    n_average_subframe_max_value = numpy.iinfo(a_subframe.dtype).max
    n_average_subframe_normalized = n_average_subframe / n_average_subframe_max_value

    a_frame = cv2.rectangle(
        a_frame,
        (n_x, n_y),
        (n_x+n_subframe_width, n_y+n_subframe_height),
        a_color,
        1
    )
    cv2.putText(
            a_frame, 
            f"avg: {n_average_subframe_normalized:.2f}",
            (n_x,n_y),
            cv2.cv2.FONT_HERSHEY_SIMPLEX, 
            0.8,
            a_color,
            1
    )

    return n_average_subframe_normalized 

def change_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def f_put_text(
    a_frame
    ):
    n_font                   = cv2.FONT_HERSHEY_SIMPLEX
    a_origin = (50,50)
    n_font_scale              = 0.8
    a_font_color             = (0,255,0)
    n_thickness              = 2
    n_line_type               = 2
    # a_frame_rgb = cv2.cvtColor(a_frame, cv2.COLOR_BGR2RGB)
    n_i = 1
    for s_text in a_s_text:
        cv2.putText(
            a_frame,
            s_text, 
            (a_origin[0], int(a_origin[1]*n_i)), 
            n_font, 
            n_font_scale,
            a_font_color,
            n_thickness,
            n_line_type
        )
        n_i+=1

def f_detect_light_sources(a_frame): 
    a_frame_singlechannel = cv2.cvtColor(a_frame, cv2.COLOR_BGR2GRAY)
    a_frame_singlechannel_blurred = cv2.GaussianBlur(a_frame_singlechannel, (11, 11), 0)
        
    a_frame_singlechannel_blurred_threshhold = cv2.threshold(
        a_frame_singlechannel_blurred,
        n_threshhold_value,
        n_threshhold_max_value,
        cv2.THRESH_BINARY
    )[1]
    a_frame_singlechannel_blurred_threshhold = cv2.erode(a_frame_singlechannel_blurred_threshhold, None, iterations=2)
    a_frame_singlechannel_blurred_threshhold = cv2.dilate(a_frame_singlechannel_blurred_threshhold, None, iterations=4)

    return a_frame_singlechannel_blurred_threshhold

def f_detect_round_shapes(a_frame):
    a_frame_singlechannel = cv2.cvtColor(a_frame, cv2.COLOR_BGR2GRAY)
    a_frame_singlechannel_blurred = cv2.GaussianBlur(a_frame_singlechannel, (11, 11), 0)
    
        # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    minDist = 100
    param1 = 30 #500
    param2 = 50 #200 #smaller value-> more false circles
    minRadius = 5
    maxRadius = 100 #10

    circles = cv2.HoughCircles(
        a_frame_singlechannel_blurred,
        cv2.HOUGH_GRADIENT,
        1,
        minDist,
        param1=param1,
        param2=param2,
        minRadius=minRadius,
        maxRadius=maxRadius
    )

    if circles is not None:
        circles = numpy.uint16(numpy.around(circles))
        for i in circles[0,:]:
            cv2.circle(a_frame_singlechannel_blurred, (i[0], i[1]), i[2], (0, 255, 0), 2)



o_camera = cv2.VideoCapture()

a_o_video_device = f_a_o_video_device()
s_o_camera_s_name_default = "hd webcam c615"

print('---')
print('available cameras')
n_index = 0
n_i = 0
for o_video_device in a_o_video_device:
    if s_o_camera_s_name_default in o_video_device.s_name.lower():
        n_index = n_i
    print(str(n_i) + " " + o_video_device.s_name)
    n_i+=1
print('---')

n_index_input = input(f"pick an available camera (default is {n_index})")

try: 
    n_index_input = int(n_index_input) 
    if(n_index_input < 0 or n_index_input > len(a_o_video_device)):
        raise Exception("n_index_input < 0 or n_index_input > len(a_o_video_device)")

    n_index = n_index_input
except: 
    pass

o_camera = a_o_video_device[n_index]

o_video_device = a_o_video_device[n_index]
for n in o_video_device.a_n_number:
    print(n)
    o_camera = cv2.VideoCapture(int(n))
    if(o_camera.isOpened()):
        break


if o_camera.isOpened() == False:
    # the camera wont always be on the same port number
    # try one of the following numbers
    # n_port_number = 1
    # n_port_number = 2
    # n_port_number = 3
    n_port_number = 5 #
    o_camera = cv2.VideoCapture(n_port_number)

codec = 0x47504A4D  # MJPG
o_camera.set(cv2.CAP_PROP_FPS, 30.0)
o_camera.set(cv2.CAP_PROP_FOURCC, codec)
o_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
o_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# o_camera = cv2.VideoCapture(n_port_number, cv2.CAP_DSHOW)
# o_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# o_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

n_threshhold_value = 100
n_threshhold_max_value = 255
s_window_name = "CHEOPS Camera"
# cv2.namedWindow(s_window_name)
n_lightness_factor = 1
n_lightness_summand = 0
a_s_text = [
    "move subframe: arrow keys (up/down/left/right)",
    "scale subframe: shift + arrow keys (up/down/left/right)",
    "average value subframe: ",
]
n_subframe_width = 100
n_subframe_height = 100

n_subframe_translation_speed = 10
n_subframe_scale_speed = 10
n_data_point_x = 0


n_measurements_per_second = 10
n_seconds_before_refresh = 30
n_width_datapoints_plot = n_seconds_before_refresh * n_measurements_per_second
n_ts_sec_delta_max = 1/n_measurements_per_second


def f_get_darker(self):
    self.a_color = (self.a_color[0],self.a_color[1]-1,self.a_color[2])
    # self.a_color[0] = self.a_color[0] -1
    # pass

# matplotlib.pyplot.axis([0, n_width_datapoints_plot, 0, 1])
# matplotlib.pyplot.title('Lightcurve')
# matplotlib.pyplot.xlabel(f"Time [1/{n_measurements_per_second} seconds]")
# matplotlib.pyplot.ylabel("Flux (quantity of light) [Normalized]")
# matplotlib.pyplot.ioff()

a_plot_points_x = numpy.array(range(0,300))
a_plot_points_y = numpy.zeros(n_width_datapoints_plot)

# a_frame_arrows = cv2.imread("./control_arrows.png", cv2.IMREAD_UNCHANGED)
# a_frame_arrows = cv2.resize(a_frame_arrows, dsize=(int(a_frame_arrows.shape[1]/2), int(a_frame_arrows.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
# a_frame_shift = cv2.imread("./control_shift_arrows.png", cv2.IMREAD_UNCHANGED)
# a_frame_shift = cv2.resize(a_frame_shift, dsize=(int(a_frame_shift.shape[1]/2), int(a_frame_shift.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
# a_frame_esc = cv2.imread("./control_esc.png", cv2.IMREAD_UNCHANGED)
# a_frame_esc = cv2.resize(a_frame_esc, dsize=(int(a_frame_esc.shape[1]/2), int(a_frame_esc.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
# a_frame_arrows = a_frame_arrows+10
# a_frame_esc = a_frame_esc+10
# a_frame_shift = a_frame_shift+10
# a_a_frame_to_blend = [
#     a_frame_esc,
#     a_frame_arrows, 
#     a_frame_shift,
# ]

b_success, a_frame = o_camera.read()
n_subframe_x = int((a_frame.shape[1] / 2) - (n_subframe_width/2) )
n_subframe_y = int((a_frame.shape[0] / 2) - (n_subframe_height/2) )





n_width_px = 1000  
n_height_px = 500  
a_frame = []  
o_cv2_text_axis_x = O_cv2_text( 
    a_color=(0,255,0), 
    s='time',
    n_font_size= 1,
    n_thickness= 1,
    n_font_type= cv2.FONT_HERSHEY_SIMPLEX
)    
o_cv2_text_axis_y = O_cv2_text( 
    a_color=(0,255,0), 
    s='light intensity',
    n_font_size= 1,
    n_thickness= 1,
    n_font_type= cv2.FONT_HERSHEY_SIMPLEX
)
n_min_y = 0
n_max_y = 1
n_min_x = 0
n_max_x = 300

o_graph = O_graph(
    n_width_px = n_width_px, 
    n_height_px = n_height_px, 
    a_frame = a_frame, 
    o_cv2_text_axis_x = o_cv2_text_axis_x, 
    o_cv2_text_axis_y = o_cv2_text_axis_y, 
    n_min_y = n_min_y,
    n_max_y = n_max_y,
    n_min_x = n_min_x,
    n_max_x = n_max_x, 
    n_markers_axis_y = 10,
    n_markers_axis_x = 10 
)

o_keyboard_key_state_freeze = O_keyboard_key_state(
    "space"
)

o_keyboard_key_state_record = O_keyboard_key_state(
    "r"
)
def f_state_toggle_function(self):
    if(self.b_state_toggle):
        print("now")
        o_graph.a_o_graph_render_object = [o for o in o_graph.a_o_graph_render_object if o.s_name != "b_record"]

o_keyboard_key_state_record.f_state_toggle_function = f_state_toggle_function 
a_o_keyboard_key_state = [
    o_keyboard_key_state_freeze, 
    o_keyboard_key_state_record
]
n_x = 0
n_y = 0

n_ts_ms_now = 0
n_ts_ms_last = 0
n_ts_ms_delta = 0

o_graph_render_object_freezed = O_graph_render_object(
        "text",
        0.5,
        0.5,
        0,
        -0.01,
        1,
        "[space] to freeze",
        (0,255,0)
        # n_alpha
    )
o_graph_render_object_record = O_graph_render_object(
        "text",
        0.5,
        0.5,
        0,
        0,
        1,
        "[r] to record",
        (0,255,0)
        # n_alpha
)
o_graph_a_o_graph_render_object_default = [
    o_graph_render_object_freezed, 
    o_graph_render_object_record
]

while 1:
    n_ts_ms_now = int(round(time.time() * 1000))
    n_ts_ms_delta = n_ts_ms_now - n_ts_ms_last
    # print(n_ts_ms_delta)

    # print(n_ts_sec)
    b_success, a_frame = o_camera.read()
    if not b_success:
        print("failed to grab frame")
        break

    # a_frame = change_brightness(a_frame, n_lightness_summand)

    n_normalized = f_n_normalized_average_in_square(
        n_center_x=n_subframe_x,
        n_center_y=n_subframe_y,
        n_width=n_subframe_width,
        n_height=n_subframe_height,
        a_frame=a_frame
    )

    # a_s_text[2] = f"average value subframe: {n_normalized:.2f}" 
    # n_x = n_x + n_ts_ms_delta
    n_y = n_normalized
    # n_y = math.sin(n_ts_ms_delta) * 0.5
    # n_y = 0.5
    # n_y = math.sin(n_ts_ms_now) * 0.5
    n_x = int(n_x + (n_ts_ms_delta/30))
    if(n_x >= n_max_x):
        n_x = 0
        a_o_graph_render_object_filtered_b_record = [o for o in o_graph.a_o_graph_render_object if o.s_name == "b_record"]

        o_graph.a_o_graph_render_object = o_graph_a_o_graph_render_object_default + a_o_graph_render_object_filtered_b_record

    o_graph_render_object = O_graph_render_object(
            "circle",
            2,
            2,
            n_x,
            n_y,
            1,
            str(n_x),
            (0,255,0)
            # n_alpha
        )
    if o_keyboard_key_state_record.b_state_toggle == False: 
        o_graph_render_object.a_color = (0,255,0)

    else:
        o_graph_render_object.s_name = "b_record"
        o_graph_render_object.a_color = (0,0,255)    
    # o_graph_render_object.f_render_function = f_get_darker

    if o_keyboard_key_state_freeze.b_state_toggle == False: 
        o_graph.a_o_graph_render_object.append(o_graph_render_object)
    
    o_graph_render_object_freezed.s_text = "[space] to "+ ( "un-freeze" if o_keyboard_key_state_freeze.b_state_toggle else "freeze")
    o_graph_render_object_record.s_text = "[r] to "+ ( "un-record" if o_keyboard_key_state_freeze.b_state_toggle else "record")


    cv2.imshow('o_graph', o_graph.f_a_rendered())
    
    # time.sleep(0.01)


    # f_detect_round_shapes(a_frame)
    # a_frame_detected = f_detect_light_sources(a_frame) 
    # f_put_text(a_frame_detected)
    # cv2.imshow(s_window_name, a_frame_detected)

    # print(a_frame_arrows.shape)
    # exit(0)

    n_y = 0
    # for a_frame_to_blend in a_a_frame_to_blend:
    #     n_height = a_frame_to_blend.shape[0]
    #     n_width = a_frame_to_blend.shape[1]
    #     a_frame_to_blend_resized = numpy.zeros((a_frame.shape[0], a_frame.shape[1], 4), numpy.uint8)
    #     a_frame_to_blend_resized[n_y:n_height+n_y, 0:n_width] = a_frame_to_blend
    #     a_frame = cv2.cvtColor(a_frame, cv2.COLOR_BGR2BGRA)
    #     a_frame = cv2.addWeighted(a_frame,1,a_frame_to_blend_resized,0.5,0)
    #     n_y = n_y + n_height

    n_circle_radius_outer = n_subframe_width
    n_circle_radius_inner = int(n_subframe_width/2)
    # get the average normalized value of the pixels inside a circle
    n_normalized_torus = f_n_normalized_average_in_torus(
        n_subframe_x, 
        n_subframe_y,
        n_circle_radius_outer, 
        n_circle_radius_inner,
        a_frame
    )

    # print(n_normalized_torus)
    
    cv2.imshow(s_window_name + " original", a_frame)
    
    # if(keyboard.is_pressed("up")):
    #     # n_threshhold_value = (n_threshhold_value + 10) % n_threshhold_max_value
    #     # n_lightness_factor = n_lightness_factor+0.01
    #     n_lightness_summand = n_lightness_summand + 10

    # if(keyboard.is_pressed("down")):
    #     # n_threshhold_value = (n_threshhold_value - 10) % n_threshhold_max_value
    #     # n_lightness_factor = n_lightness_factor-0.01
    #     n_lightness_summand = n_lightness_summand - 10
    for o_keyboard_key_state in a_o_keyboard_key_state: 
        if(keyboard.is_pressed(o_keyboard_key_state.s_key)):
            if o_keyboard_key_state.b_key_down == False:
                o_keyboard_key_state.b_state_toggle = not o_keyboard_key_state.b_state_toggle
                o_keyboard_key_state.f_state_toggle_function(o_keyboard_key_state)

            o_keyboard_key_state.b_key_down = True
        else:
            o_keyboard_key_state.b_key_down = False


    if(keyboard.is_pressed("shift") == False):
        if(keyboard.is_pressed("up")):
            n_subframe_y = (n_subframe_y - n_subframe_translation_speed)
            if(n_subframe_y < 0):
                n_subframe_y = 0
        if(keyboard.is_pressed("down")):
            n_subframe_y = (n_subframe_y + n_subframe_translation_speed) % a_frame.shape[0]
        if(keyboard.is_pressed("left")):
            n_subframe_x = (n_subframe_x - n_subframe_translation_speed)
            if(n_subframe_x < 0):
                n_subframe_x = 0
        if(keyboard.is_pressed("right")):
            n_subframe_x = (n_subframe_x + n_subframe_translation_speed) % a_frame.shape[1]

    if(keyboard.is_pressed("shift") == True):
        if(keyboard.is_pressed("up")):
            n_subframe_height = max(1,(n_subframe_height - n_subframe_scale_speed))
        if(keyboard.is_pressed("down")):
            n_subframe_height = (n_subframe_height + n_subframe_scale_speed) % a_frame.shape[1]
        if(keyboard.is_pressed("left")):
            n_subframe_width = max(1,(n_subframe_width - n_subframe_scale_speed))
        if(keyboard.is_pressed("right")):
            n_subframe_width = (n_subframe_width + n_subframe_scale_speed) % a_frame.shape[0]

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    if(keyboard.is_pressed("esc")):
        break
    if cv2.getWindowProperty(s_window_name,cv2.WND_PROP_VISIBLE) < 1:        
        break   

    n_ts_ms_last = n_ts_ms_now


matplotlib.pyplot.close()
o_camera.release()

cv2.destroyAllWindows()


