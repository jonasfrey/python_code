import cv2
from scipy import signal
from scipy import misc
import numpy
import pyautogui
s_path_file_original = "./moon_original.png"
s_path_file_translated_x_y = "./moon_translated_x_y.png"

a_img_original = cv2.imread(s_path_file_original)
a_img_original_grayscale = cv2.cvtColor(a_img_original, cv2.COLOR_BGR2GRAY)

a_img_translated_x_y = cv2.imread(s_path_file_translated_x_y)
a_img_translated_x_y_grayscale = cv2.cvtColor(a_img_translated_x_y, cv2.COLOR_BGR2GRAY)

# a_img_correlated = signal.correlate2d(a_img_original_grayscale, a_img_translated_x_y_grayscale)

# a_img_correlated = xcorr2(a_img_original_grayscale, a_img_translated_x_y_grayscale)

# a_img_correlated = numpy.cov(a_img_original_grayscale, a_img_translated_x_y_grayscale)
# a_img_correlated = numpy.cov(a_img_original_grayscale, a_img_original_grayscale)

s_window_name = "asdf"

n_width = a_img_original.shape[1]
n_height = a_img_original.shape[0]
n_translate_x = 100
n_translate_y = 20
a_transformation_matrix = numpy.float32([[1,0,n_translate_x],[0,1,n_translate_y]])
a_img_original_transformed = cv2.warpAffine(a_img_original,a_transformation_matrix,(n_width,n_height))

a_screen_size = pyautogui.size()
n_screen_width = a_screen_size[0]
n_screen_height = a_screen_size[1]

while(True):
    a_pos_mouse = pyautogui.position()
    n_mouse_x_normalized = float(a_pos_mouse[0] / n_screen_width)
    n_mouse_y_normalized = float(a_pos_mouse[1] / n_screen_height)

    n_translate_x = n_mouse_x_normalized * 500
    n_translate_y = n_mouse_y_normalized * 500
    
    a_transformation_matrix = numpy.float32([[1,0,n_translate_x],[0,1,n_translate_y]])
    a_img_original_transformed = cv2.warpAffine(a_img_original,a_transformation_matrix,(n_width,n_height))
    a_img_difference = a_img_original - a_img_original_transformed


    a_img_original_transformed_grayscale = cv2.cvtColor(a_img_original_transformed, cv2.COLOR_BGR2GRAY)
    a_img_correlated = numpy.cov(a_img_original_transformed_grayscale, a_img_translated_x_y_grayscale)

    cv2.imshow(s_window_name, a_img_correlated)
    n_sum = numpy.sum(a_img_difference)
    print(n_sum)
    cv2.waitKey(1)

    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty(s_window_name, cv2.WND_PROP_VISIBLE) <1:
        break

cv2.destroyAllWindows()