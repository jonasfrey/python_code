from copyreg import constructor
import cv2
import numpy
import keyboard
import matplotlib.pyplot
# using time module
import math
import time
import random

def f_n_normalized_average_in_torus(
    n_circles_center_x, 
    n_circles_center_y,
    n_circle_radius_outer, 
    n_circle_radius_inner,
    a_frame
):
    n_normalized_average_outer = f_n_normalized_average_in_circle(
        n_circles_center_x, 
        n_circles_center_y,
        n_circle_radius_outer, 
        a_frame
    )
    n_normalized_average_inner = f_n_normalized_average_in_circle(
        n_circles_center_x, 
        n_circles_center_y,
        n_circle_radius_inner, 
        a_frame
    )
    n_normalized_average_torus = n_normalized_average_outer - n_normalized_average_inner
    return n_normalized_average_torus


def f_n_normalized_average_in_circle(
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
    cv2.circle(
        a_frame,
        (n_circle_center_x,n_circle_center_y),
        n_circle_radius,
        (0,255,0),
    )
    a_masked = cv2.bitwise_and(a_frame, a_frame, mask=a_mask)
    # cv2.imshow("f_n_normalized_average_in_circle a_masked", a_masked)

    n_number_of_pixels_in_circle = int(n_circle_radius * n_circle_radius * (math.pi))
    n_normalized = numpy.sum(a_masked) / n_number_of_pixels_in_circle
    return n_normalized 

def f_n_normalized_average_in_square(
    n_center_x, 
    n_center_y,
    n_width,
    n_height,
    a_frame
):
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
        (0,255,0),
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

# the camera wont always be on the same port number
# try one of the following numbers
# n_port_number = 1
# n_port_number = 2
# n_port_number = 3
n_port_number = 5
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
cv2.namedWindow(s_window_name)
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

n_ts_sec = time.time()
n_ts_sec_last = time.time()
n_ts_sec_delta = 0
n_measurements_per_second = 10
n_seconds_before_refresh = 30
n_width_datapoints_plot = n_seconds_before_refresh * n_measurements_per_second
n_ts_sec_delta_max = 1/n_measurements_per_second

matplotlib.pyplot.axis([0, n_width_datapoints_plot, 0, 1])
matplotlib.pyplot.title('Lightcurve')
matplotlib.pyplot.xlabel(f"Time [1/{n_measurements_per_second} seconds]")
matplotlib.pyplot.ylabel("Flux (quantity of light) [Normalized]")
matplotlib.pyplot.ioff()

a_plot_points_x = numpy.array(range(0,300))
a_plot_points_y = numpy.zeros(n_width_datapoints_plot)

a_frame_arrows = cv2.imread("./control_arrows.png", cv2.IMREAD_UNCHANGED)
a_frame_arrows = cv2.resize(a_frame_arrows, dsize=(int(a_frame_arrows.shape[1]/2), int(a_frame_arrows.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
a_frame_shift = cv2.imread("./control_shift_arrows.png", cv2.IMREAD_UNCHANGED)
a_frame_shift = cv2.resize(a_frame_shift, dsize=(int(a_frame_shift.shape[1]/2), int(a_frame_shift.shape[0]/2)), interpolation=cv2.INTER_CUBIC)
a_frame_esc = cv2.imread("./control_esc.png", cv2.IMREAD_UNCHANGED)
a_frame_esc = cv2.resize(a_frame_esc, dsize=(int(a_frame_esc.shape[1]/2), int(a_frame_esc.shape[0]/2)), interpolation=cv2.INTER_CUBIC)

a_a_frame_to_blend = [
    a_frame_esc,
    a_frame_arrows, 
    a_frame_shift,
]

b_success, a_frame = o_camera.read()
n_subframe_x = int((a_frame.shape[1] / 2) - (n_subframe_width/2) )
n_subframe_y = int((a_frame.shape[0] / 2) - (n_subframe_height/2) )

a_frame_graph = numpy.zeros(a_frame.shape)
n_graph_size_factor = 0.9
n_graph_height = int(a_frame_graph.shape[0] * n_graph_size_factor)
n_graph_width = int(a_frame_graph.shape[1] * n_graph_size_factor)
n_graph_x =  int((a_frame_graph.shape[1] - n_graph_width) /2)
n_graph_y = int((a_frame_graph.shape[0] - n_graph_height) /2)




while True:
    # time.sleep(n_ts_sec_delta_max/2)
    n_ts_sec = time.time()
    if(n_ts_sec - n_ts_sec_last > n_ts_sec_delta_max):
        n_ts_sec_last = n_ts_sec
        print(n_ts_sec)
        b_success, a_frame = o_camera.read()
        # a_frame = a_frame * n_lightness_factor # not working
        # a_frame = a_frame + n_lightness_summand
        a_frame = change_brightness(a_frame, n_lightness_summand)

        n_normalized = f_n_normalized_average_in_square(
            n_center_x=n_subframe_x,
            n_center_y=n_subframe_y,
            n_width=n_subframe_width,
            n_height=n_subframe_height,
            a_frame=a_frame
        )
        a_plot_points_x[n_data_point_x] =  n_data_point_x
        a_plot_points_y[n_data_point_x] = n_normalized

        n_data_point_x = (n_data_point_x + 1) % n_width_datapoints_plot
        if(n_data_point_x == 0):
            a_plot_points_x = numpy.zeros(n_width_datapoints_plot)
            a_plot_points_y = numpy.zeros(n_width_datapoints_plot)
            matplotlib.pyplot.clf()
            matplotlib.pyplot.axis([0, n_width_datapoints_plot, 0, 1])
            a_frame_graph = numpy.zeros(a_frame.shape)

        n_a_frame_graph_x = int((n_graph_width/n_width_datapoints_plot*n_data_point_x) + n_graph_x)
        n_a_frame_graph_y = int((n_graph_height*n_normalized) + n_graph_y)

        # a_frame = cv2.rectangle(
        #     a_frame_graph,
        #     (n_graph_x, n_graph_y),
        #     (n_graph_width, n_graph_height),
        #     (0,255,0),
        #     1
        # )
        cv2.circle(
            a_frame_graph,
            (n_a_frame_graph_x, n_a_frame_graph_y),
            1,
            (0,255,0),
            1
        ) 
        cv2.imshow("adsf", a_frame_graph)

        # matplotlib.pyplot.scatter(
        #     a_plot_points_x[n_data_point_x-1],
        #     a_plot_points_y[n_data_point_x-1],
        #     c='r'
        # )
        # matplotlib.pyplot.plot(
        #     a_plot_points_x,
        #     a_plot_points_y,
        #     c='r'
        # )
        # matplotlib.pyplot.plot(
        #     a_plot_points_x,
        #     a_plot_points_y,
        #     ".",
        #     # # linestyle="",
        #     #marker="o",
        #     # markersize = 10, 
        #     color='green'
        # )
        # matplotlib.pyplot.show(block=False)
        matplotlib.pyplot.pause(0.001)
        # print(n_average_subframe_normalized)

        a_s_text[2] = f"average value subframe: {n_normalized:.2f}" 
        # a_s_text[2] = str(str("average value subframe: ") + str(n)),
        # Using cv2.rectangle() method
        # Draw a rectangle with blue line borders of thickness of 2 px

        
        # print(a_frame)


        if not b_success:
            print("failed to grab frame")
            break

        # f_detect_round_shapes(a_frame)
        a_frame_detected = f_detect_light_sources(a_frame) 

        # f_put_text(a_frame_detected)
        cv2.imshow(s_window_name, a_frame_detected)

        # print(a_frame_arrows.shape)
        # exit(0)
        n_y = 0
        for a_frame_to_blend in a_a_frame_to_blend:
            n_height = a_frame_to_blend.shape[0]
            n_width = a_frame_to_blend.shape[1]
            a_frame_to_blend_resized = numpy.zeros((a_frame.shape[0], a_frame.shape[1], 4), numpy.uint8)
            a_frame_to_blend_resized[n_y:n_height+n_y, 0:n_width] = a_frame_to_blend
            a_frame = cv2.cvtColor(a_frame, cv2.COLOR_BGR2BGRA)
            a_frame = cv2.addWeighted(a_frame,1,a_frame_to_blend_resized,0.5,0)
            n_y = n_y + n_height

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
        
        cv2.circle(a_frame, (n_subframe_x,n_subframe_y), n_subframe_width, (0,255,0,1), 1)
        cv2.imshow(s_window_name + " original", a_frame)
        
        # if(keyboard.is_pressed("up")):
        #     # n_threshhold_value = (n_threshhold_value + 10) % n_threshhold_max_value
        #     # n_lightness_factor = n_lightness_factor+0.01
        #     n_lightness_summand = n_lightness_summand + 10

        # if(keyboard.is_pressed("down")):
        #     # n_threshhold_value = (n_threshhold_value - 10) % n_threshhold_max_value
        #     # n_lightness_factor = n_lightness_factor-0.01
        #     n_lightness_summand = n_lightness_summand - 10

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
                n_subframe_height = (n_subframe_height - n_subframe_scale_speed) % a_frame.shape[1]
            if(keyboard.is_pressed("down")):
                n_subframe_height = (n_subframe_height + n_subframe_scale_speed) % a_frame.shape[1]
            if(keyboard.is_pressed("left")):
                n_subframe_width = (n_subframe_width - n_subframe_scale_speed) % a_frame.shape[0]
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


matplotlib.pyplot.close()
o_camera.release()

cv2.destroyAllWindows()


