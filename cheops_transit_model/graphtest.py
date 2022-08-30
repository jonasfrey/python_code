import cv2
import math
import time
from O_graph import O_graph, O_graph_datapoint
from O_cv2_text import O_cv2_text


n_width_px = 1000  
n_height_px = 500  
a_frame = []  
o_cv2_text_axis_x = O_cv2_text( 
    a_color=(0,255,0), 
    s='test x',
    n_font_size= 1,
    n_thickness= 1,
    n_font_type= cv2.FONT_HERSHEY_COMPLEX
)    
o_cv2_text_axis_y = O_cv2_text( 
    a_color=(0,255,0), 
    s='flux [light intensity]',
    n_font_size= 1,
    n_thickness= 1,
    n_font_type= cv2.FONT_HERSHEY_COMPLEX
)  
n_min_y = 10 
n_max_y = 100 
n_min_x = -10 
n_max_x = 100

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

n_i = 0

n_amp = (o_graph.n_max_y/2) * 0.1
n_q = (o_graph.n_max_y/2)
n_freq = 0.1
n_time = 0
while(n_i < 1000): 
    n_i+=1
    n_time += n_freq
    n_y = math.sin(n_time) * n_amp + n_q
    n_x = n_time
    o_graph.o_cv2_text_axis_x.s = str(time.time())
    o_graph.f_add_data_point(
        O_graph_datapoint(
            n_x,
            n_y,
            O_cv2_text( 
                a_color=(0,255,0), 
                s=str(n_x),
                n_font_size= 1,
                n_thickness= 1,
                n_font_type= cv2.FONT_HERSHEY_COMPLEX
            ), 
            O_cv2_text( 
                a_color=(0,255,0), 
                s=str(n_y),
                n_font_size= 1,
                n_thickness= 1,
                n_font_type= cv2.FONT_HERSHEY_COMPLEX
            )  
        )
    )
    cv2.imshow('o_graph', o_graph.f_a_rendered())
    time.sleep(0.01)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break