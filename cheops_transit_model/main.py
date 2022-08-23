import cv2
import numpy
import keyboard
import matplotlib.pyplot

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
n_subframe_x = 0
n_subframe_y = 0
n_subframe_width = 100
n_subframe_height = 100
n_subframe_translation_speed = 10
n_subframe_scale_speed = 10
n_width_datapoints_plot = 100
n_data_point_x = 0
a_plot_points_x = numpy.zeros(n_width_datapoints_plot)
a_plot_points_y = numpy.zeros(n_width_datapoints_plot)

matplotlib.style.use('classic')
# Define and update plot

matplotlib.pyplot.axis([0, n_width_datapoints_plot, 0, 1])

while True:
    b_success, a_frame = o_camera.read()
    # a_frame = a_frame * n_lightness_factor # not working
    # a_frame = a_frame + n_lightness_summand
    a_frame = change_brightness(a_frame, n_lightness_summand)
    a_subframe = a_frame[n_subframe_y:n_subframe_y+n_subframe_height,n_subframe_x:n_subframe_x+n_subframe_width]
    n_average_subframe = numpy.average(a_subframe)
    n_average_subframe_max_value = numpy.iinfo(a_subframe.dtype).max
    n_average_subframe_normalized = n_average_subframe / n_average_subframe_max_value
    a_plot_points_x[n_data_point_x] =  n_data_point_x
    a_plot_points_y[n_data_point_x] = n_average_subframe_normalized

    n_data_point_x = (n_data_point_x + 1) % n_width_datapoints_plot
    if(n_data_point_x == 0):
        a_plot_points_x = numpy.zeros(n_width_datapoints_plot)
        a_plot_points_y = numpy.zeros(n_width_datapoints_plot)
        matplotlib.pyplot.clf()
        matplotlib.pyplot.axis([0, n_width_datapoints_plot, 0, 1])

    matplotlib.pyplot.plot(
        a_plot_points_x,
        a_plot_points_y,
        linestyle="",
        marker="o", 
        color='green'
    )
    # matplotlib.pyplot.show(block=False)
    matplotlib.pyplot.pause(0.05)
    print(n_average_subframe_normalized)

    a_s_text[2] = f"average value subframe: {n_average_subframe_normalized:.2f}" 
    # a_s_text[2] = str(str("average value subframe: ") + str(n)),
    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    a_frame = cv2.rectangle(
        a_frame,
        (n_subframe_x, n_subframe_y),
        (n_subframe_x+n_subframe_width, n_subframe_y+n_subframe_height),
        (0,255,0),
        2
        )
    
    # print(a_frame)


    if not b_success:
        print("failed to grab frame")
        break

    # f_detect_round_shapes(a_frame)
    a_frame_detected = f_detect_light_sources(a_frame) 

    f_put_text(a_frame_detected)
    cv2.imshow(s_window_name, a_frame_detected)
    f_put_text(a_frame)
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


