import rawpy 
import cv2
import numpy
import pyautogui

    
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
o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
cv2.imshow(s_path_file_name, o_img_raw_resized*1)
keyCode = cv2.waitKey(1)

# exit()
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized, cv2.COLOR_BAYER_BG2BGR)
# o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)
# o_img_raw_resized = cv2.merge([o_img_raw_resized,o_img_raw_resized,o_img_raw_resized])

def f_cv2_put_text(
    a_s_line,
    a_img
    ):

    n_font = cv2.FONT_HERSHEY_SIMPLEX
    # n_font = cv2.FONT_HERSHEY_PLAIN
    a_point = (50, 50)
    a_color = (0,0,int(0.3*n_value_max))
    a_color_outline = (0,0,int(0.1*n_value_max))
    n_thickness = 2
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
        cv2.putText(
                a_img,
                s_line,
                a_point,
                n_font,
                n_font_scale,
                a_color_outline,
                thickness = n_thickness+3
            )
        cv2.putText(
                a_img,
                s_line,
                a_point,
                n_font,
                n_font_scale,
                a_color,
                thickness = n_thickness
            )

# print(o_img_raw_resized.ndim)
n_factor = 2
s_window_name = "o_img_raw_resized"
while True: 
    o_img_raw_copy = o_img_raw_resized.copy()

    a_pos_mouse = pyautogui.position()
    a_s_line = []
    a_s_line.append('x:'+str(a_pos_mouse[0]))
    a_s_line.append('y:'+str(a_pos_mouse[1]))
    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    f_cv2_put_text(a_s_line, o_img_raw_copy)
    # o_img_raw_resized = cv2.cvtColor(o_img_raw_resized,cv2.COLOR_GRAY2RGB)

    cv2.imshow(s_window_name, o_img_raw_copy*n_factor)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
            break

cv2.destroyAllWindows()